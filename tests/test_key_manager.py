import pytest # type: ignore
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the modules to test
from keyctl.core.key_manager import KeyManager
from keyctl.security.key_security import KeySecurity
from keyctl.utils.config import Config
from keyctl.utils.logger import KeyCtlError, ConfigError, SecurityError, ValidationError

# Test fixtures
@pytest.fixture
def temp_ssh_dir(tmp_path):
    """Create a temporary SSH directory."""
    ssh_dir = tmp_path / ".ssh"
    ssh_dir.mkdir()
    return ssh_dir

@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / ".keyctl.json"
    config_file.write_text("{}")
    return config_file

@pytest.fixture
def key_manager(temp_ssh_dir, temp_config_file):
    """Create a KeyManager instance with temporary paths."""
    with patch('keyctl.core.key_manager.SSH_DIR', temp_ssh_dir), \
         patch('keyctl.core.key_manager.CONFIG_PATH', temp_config_file):
        return KeyManager()

# Test key creation
def test_create_ssh_key(key_manager):
    """Test SSH key creation."""
    key_name = "test_key"
    key_type = "ed25519"
    comment = "test comment"
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = key_manager.create_key(key_name, key_type, comment)
        
        assert result.success
        assert mock_run.call_count == 2  # ssh-keygen and ssh-add
        
        # Verify key path
        key_path = key_manager.ssh_dir / key_name
        assert str(key_path) in mock_run.call_args_list[0].args[0]

# Test key security
def test_key_security_permissions(key_manager):
    """Test key permission validation."""
    key_path = key_manager.ssh_dir / "test_key"
    key_path.touch()
    os.chmod(key_path, 0o600)
    
    security = KeySecurity()
    assert security.check_permissions(key_path)
    
    # Test incorrect permissions
    os.chmod(key_path, 0o644)
    assert not security.check_permissions(key_path)

# Test key expiration
def test_key_expiration(key_manager, tmp_path):
    """Test key expiration functionality."""
    # Test setting expiration
    success, message = key_manager.config.set_key_expiration("test_key", 30)
    assert success
    assert "Set 30 days expiration" in message
    
    # Test checking expirations
    expiring = key_manager.config.check_key_expirations()
    assert "test_key" in expiring
    assert 0 < expiring["test_key"] <= 30
    
    # Test removing expiration
    success, message = key_manager.config.remove_key_expiration("test_key")
    assert success
    assert "Removed expiration" in message
    
    # Test checking empty expirations
    expiring = key_manager.config.check_key_expirations()
    assert not expiring

# Test key usage tracking
def test_key_usage_tracking(key_manager):
    """Test key usage statistics tracking."""
    key_name = "test_key"
    
    # Track key usage
    key_manager.update_key_usage(key_name)
    
    # Verify usage was recorded
    config = Config.load()
    assert key_name in config["key_usage"]
    assert config["key_usage"][key_name]["use_count"] == 1
    
    # Track another usage
    key_manager.update_key_usage(key_name)
    config = Config.load()
    assert config["key_usage"][key_name]["use_count"] == 2

# Test provider validation
def test_provider_validation(key_manager):
    """Test SSH key validation with different providers."""
    providers = ["github.com", "gitlab.com", "bitbucket.org"]
    
    for provider in providers:
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stderr=f"Successfully authenticated to {provider}"
            )
            
            result = key_manager.validate_key(provider)
            assert result.success
            assert provider in mock_run.call_args_list[0].args[0]

# Test backup functionality
def test_backup_restore(key_manager, tmp_path):
    """Test backup and restore functionality."""
    # Create test key
    test_key = key_manager.ssh_dir / "test_key"
    test_key.touch()
    os.chmod(test_key, 0o600)
    
    # Create backup
    backup_dir = tmp_path / "backup"
    result = key_manager.backup_keys(backup_dir)
    assert result.success
    assert (backup_dir / "test_key").exists()
    
    # Delete original
    test_key.unlink()
    assert not test_key.exists()
    
    # Restore
    result = key_manager.restore_keys(backup_dir)
    assert result.success
    assert test_key.exists()
    assert oct(test_key.stat().st_mode)[-3:] == '600'

# Test SSH config management
def test_ssh_config_management(key_manager, tmp_path):
    """Test SSH config management functionality."""
    # Test getting empty config
    config = key_manager.get_ssh_config()
    assert config == {}
    
    # Test adding host config
    success, message = key_manager.update_ssh_config(
        host="github.com",
        key="~/.ssh/id_ed25519",
        user="git",
        port=22
    )
    assert success
    assert "Updated SSH config" in message
    
    # Test getting updated config
    config = key_manager.get_ssh_config()
    assert "github.com" in config
    assert config["github.com"]["IdentityFile"] == "~/.ssh/id_ed25519"
    assert config["github.com"]["User"] == "git"
    assert config["github.com"]["Port"] == "22"
    
    # Test removing host config
    success, message = key_manager.remove_ssh_config("github.com")
    assert success
    assert "Removed" in message
    
    # Test getting empty config again
    config = key_manager.get_ssh_config()
    assert config == {}

# Test repository management
def test_repository_management(key_manager, tmp_path):
    """Test repository management functionality."""
    # Test linking repository
    success, message = key_manager.config.link_repo_key(
        "git@github.com:test/repo.git",
        "test_key"
    )
    assert success
    assert "Linked" in message
    
    # Test getting repository links
    links = key_manager.config.get_repo_links()
    assert "git@github.com:test/repo.git" in links
    assert links["git@github.com:test/repo.git"] == "test_key"
    
    # Test filtering links
    links = key_manager.config.get_repo_links(key="test_key")
    assert len(links) == 1
    assert "test_key" in links.values()

# Test error handling
def test_error_handling(key_manager, tmp_path):
    """Test error handling in KeyManager."""
    # Test invalid SSH config
    with patch('builtins.open', side_effect=PermissionError):
        config = key_manager.get_ssh_config()
        assert config == {}
    
    # Test invalid expiration date
    with pytest.raises(ValueError):
        key_manager.config.set_key_expiration("test_key", -1)
    
    # Test invalid repository URL
    with pytest.raises(ValidationError):
        key_manager.config.link_repo_key("invalid-url", "test_key") 
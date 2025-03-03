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
def test_key_expiration(key_manager):
    """Test key expiration functionality."""
    key_name = "test_key"
    expiry_days = 7
    
    # Set expiration
    key_manager.set_key_expiration(key_name, expiry_days)
    
    # Verify expiration was set
    config = Config.load()
    assert key_name in config["key_expiration"]
    
    # Check expiration status
    is_expired = key_manager.check_key_expiration(key_name)
    assert not is_expired  # Should not be expired yet
    
    # Test expired key
    past_date = datetime.now() - timedelta(days=1)
    config["key_expiration"][key_name] = past_date.isoformat()
    Config.save(config)
    
    is_expired = key_manager.check_key_expiration(key_name)
    assert is_expired

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
    """Test SSH config file management."""
    config_file = key_manager.ssh_dir / "config"
    
    # Add host
    host_config = {
        "HostName": "github.com",
        "User": "git",
        "IdentityFile": "~/.ssh/github_key"
    }
    
    key_manager.add_ssh_config("github.com", host_config)
    
    # Verify config was written
    assert config_file.exists()
    content = config_file.read_text()
    assert "github.com" in content
    assert "IdentityFile" in content
    
    # Read config
    configs = key_manager.parse_ssh_config()
    assert "github.com" in configs
    assert configs["github.com"]["identityfile"] == "~/.ssh/github_key"

# Test error handling
def test_error_handling(key_manager):
    """Test error handling in various scenarios."""
    
    # Test invalid key type
    with pytest.raises(ValueError):
        key_manager.create_key("test_key", "invalid_type")
    
    # Test invalid permissions
    with patch('os.chmod') as mock_chmod:
        mock_chmod.side_effect = PermissionError()
        result = key_manager.fix_permissions(Path("test_key"))
        assert not result.success
        assert "permission denied" in result.error.lower()
    
    # Test network errors
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = ConnectionError()
        result = key_manager.validate_key("github.com")
        assert not result.success
        assert "connection error" in result.error.lower() 
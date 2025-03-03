"""Configuration management for SSH key manager."""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from .logger import get_logger

logger = get_logger(__name__)

class Config:
    """Manages configuration and persistent data for SSH key manager."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".ssh" / ".keyctl"
        self.config_file = self.config_dir / "config.json"
        self.usage_file = self.config_dir / "usage.json"
        self._ensure_config_dir()
        self._load_config()

    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.config_dir.chmod(0o700)  # Secure permissions
        except Exception as e:
            logger.error(f"Error creating config directory: {e}")
            raise

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                self.config = json.loads(self.config_file.read_text())
            else:
                self.config = self._create_default_config()
                self._save_config()
                
            if self.usage_file.exists():
                self.usage = json.loads(self.usage_file.read_text())
            else:
                self.usage = {}
                self._save_usage()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        return {
            "default_key_type": "ed25519",
            "default_key_comment": "",
            "key_expiry_days": 90,  # Default key rotation period
            "providers": {
                "github.com": {
                    "test_command": "ssh -T git@github.com",
                    "success_message": "successfully authenticated"
                },
                "gitlab.com": {
                    "test_command": "ssh -T git@gitlab.com",
                    "success_message": "Welcome to GitLab"
                },
                "bitbucket.org": {
                    "test_command": "ssh -T git@bitbucket.org",
                    "success_message": "logged in as"
                }
            }
        }

    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            self.config_file.write_text(json.dumps(self.config, indent=4))
            self.config_file.chmod(0o600)  # Secure permissions
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise

    def _save_usage(self) -> None:
        """Save usage data to file."""
        try:
            self.usage_file.write_text(json.dumps(self.usage, indent=4))
            self.usage_file.chmod(0o600)  # Secure permissions
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")
            raise

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self._save_config()

    def update_key_usage(self, key_name: str) -> None:
        """Update usage statistics for a key."""
        now = datetime.now().isoformat()
        if key_name not in self.usage:
            self.usage[key_name] = {
                "created": now,
                "last_used": now,
                "use_count": 1
            }
        else:
            self.usage[key_name]["last_used"] = now
            self.usage[key_name]["use_count"] += 1
        self._save_usage()

    def get_key_usage(self, key_name: str) -> Optional[Dict[str, Any]]:
        """Get usage statistics for a key."""
        return self.usage.get(key_name)

    def set_key_expiration(self, key_name: str, days: Optional[int] = None) -> None:
        """Set expiration date for a key."""
        if days is None:
            days = self.config["key_expiry_days"]
            
        expiry_date = (datetime.now() + timedelta(days=days)).isoformat()
        if key_name not in self.usage:
            self.usage[key_name] = {"created": datetime.now().isoformat()}
        self.usage[key_name]["expiry"] = expiry_date
        self._save_usage()

    def get_key_expiration(self, key_name: str) -> Optional[str]:
        """Get expiration date for a key."""
        usage = self.usage.get(key_name, {})
        return usage.get("expiry")

    def get_provider_config(self, provider: str) -> Optional[Dict[str, str]]:
        """Get provider-specific configuration."""
        return self.config["providers"].get(provider) 
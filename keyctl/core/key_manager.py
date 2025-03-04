"""Core key management functionality."""
from pathlib import Path
import subprocess
from typing import Optional, Dict, List, Tuple
from datetime import datetime

from ..security.key_security import KeySecurity
from ..utils.config import Config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class KeyManager:
    """Manages SSH key operations and lifecycle."""

    def __init__(self, ssh_dir: Path = Path.home() / ".ssh"):
        self.ssh_dir = ssh_dir
        self.security = KeySecurity()
        self.config = Config()

    def create_key(self, name: str, key_type: str = "ed25519", 
                  comment: Optional[str] = None) -> Tuple[bool, str]:
        """Create a new SSH key."""
        key_path = self.ssh_dir / name
        
        if key_path.exists():
            return False, "Key already exists"
            
        try:
            cmd = ["ssh-keygen", "-t", key_type, "-f", str(key_path)]
            if comment:
                cmd.extend(["-C", comment])
                
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Set proper permissions
            self.security.fix_permissions(key_path)
            
            # Add to agent
            self.add_to_agent(key_path)
            
            return True, "Key created successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Key creation failed: {e.stderr}"
        except Exception as e:
            return False, f"Error creating key: {str(e)}"

    def add_to_agent(self, key_path: Path) -> bool:
        """Add a key to the SSH agent."""
        try:
            if not self.security.check_permissions(key_path):
                return False
                
            subprocess.run(["ssh-add", str(key_path)], 
                         capture_output=True, text=True, check=True)
            
            # Update usage statistics
            self.config.update_key_usage(key_path.name)
            
            return True
        except subprocess.CalledProcessError:
            return False

    def remove_from_agent(self, key_path: Optional[Path] = None) -> bool:
        """Remove a key or all keys from the SSH agent."""
        try:
            if key_path:
                subprocess.run(["ssh-add", "-d", str(key_path)], 
                             capture_output=True, text=True, check=True)
            else:
                subprocess.run(["ssh-add", "-D"], 
                             capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_keys(self) -> List[Path]:
        """List all SSH keys in the SSH directory."""
        return [key for key in self.ssh_dir.glob("id_*") 
                if key.suffix == "" and key.name != "id_ed25519_sk"]

    def validate_key(self, provider: str) -> Tuple[bool, str]:
        """Validate a key with a specific provider."""
        try:
            test_url = f"git@{provider}"
            result = subprocess.run(["ssh", "-T", test_url], 
                                 capture_output=True, text=True)
            
            # Check provider-specific success messages
            success_messages = {
                "github.com": "successfully authenticated",
                "gitlab.com": "Welcome to GitLab",
                "bitbucket.org": "logged in as",
            }
            
            success_msg = success_messages.get(provider, "")
            if success_msg and success_msg in result.stderr:
                return True, "Authentication successful"
                
            return False, f"Authentication failed: {result.stderr}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def get_key_info(self, key_path: Path) -> Dict:
        """Get detailed information about a key."""
        info = {
            "name": key_path.name,
            "type": None,
            "comment": None,
            "last_used": None,
            "expiry": None,
            "permissions": oct(key_path.stat().st_mode)[-3:],
        }
        
        # Get key type and comment from public key
        pub_key_path = Path(f"{key_path}.pub")
        if pub_key_path.exists():
            try:
                content = pub_key_path.read_text()
                parts = content.strip().split()
                if len(parts) >= 2:
                    info["type"] = parts[0].replace("ssh-", "")
                if len(parts) >= 3:
                    info["comment"] = " ".join(parts[2:])
            except Exception as e:
                logger.error(f"Error reading public key: {e}")
        
        # Get usage information
        usage = self.config.get_key_usage(key_path.name)
        if usage:
            info["last_used"] = usage.get("last_used")
            
        # Get expiration
        expiry = self.config.get_key_expiration(key_path.name)
        if expiry:
            info["expiry"] = expiry
            
        return info

    def rotate_key(self, key_path: Path) -> Tuple[bool, str]:
        """Rotate an SSH key while preserving metadata."""
        try:
            # Get current key info
            old_info = self.get_key_info(key_path)
            
            # Create backup
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = key_path.with_suffix(f".bak_{backup_suffix}")
            key_path.rename(backup_path)
            
            # Create new key with same properties
            success, message = self.create_key(
                key_path.name,
                old_info["type"] or "ed25519",
                old_info["comment"]
            )
            
            if not success:
                # Restore backup if creation failed
                backup_path.rename(key_path)
                return False, f"Key rotation failed: {message}"
                
            return True, "Key rotated successfully"
        except Exception as e:
            return False, f"Error rotating key: {str(e)}"

    def get_ssh_config(self) -> Dict[str, Dict[str, str]]:
        """Get the current SSH config."""
        config_path = Path.home() / ".ssh" / "config"
        if not config_path.exists():
            return {}
            
        config = {}
        current_host = None
        
        try:
            with open(config_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                        
                    if line.lower().startswith("host "):
                        current_host = line.split()[1]
                        config[current_host] = {}
                    elif current_host and " " in line:
                        key, value = line.split(" ", 1)
                        config[current_host][key] = value
                        
            return config
        except Exception as e:
            logger.error(f"Error reading SSH config: {e}")
            return {}
            
    def update_ssh_config(
        self,
        host: str,
        key: Optional[str] = None,
        user: Optional[str] = None,
        port: Optional[int] = None
    ) -> Tuple[bool, str]:
        """Update SSH config for a host."""
        config_path = Path.home() / ".ssh" / "config"
        config_dir = config_path.parent
        
        try:
            # Create .ssh directory if it doesn't exist
            config_dir.mkdir(parents=True, exist_ok=True)
            
            # Read existing config
            config = self.get_ssh_config()
            
            # Update host settings
            if host not in config:
                config[host] = {}
                
            if key:
                config[host]["IdentityFile"] = key
            if user:
                config[host]["User"] = user
            if port:
                config[host]["Port"] = str(port)
                
            # Write updated config
            with open(config_path, "w") as f:
                for host_name, settings in config.items():
                    f.write(f"Host {host_name}\n")
                    for key, value in settings.items():
                        f.write(f"    {key} {value}\n")
                    f.write("\n")
                    
            return True, f"Updated SSH config for {host}"
        except Exception as e:
            error_msg = f"Error updating SSH config: {e}"
            logger.error(error_msg)
            return False, error_msg
            
    def remove_ssh_config(self, host: str) -> Tuple[bool, str]:
        """Remove host from SSH config."""
        config_path = Path.home() / ".ssh" / "config"
        
        try:
            # Read existing config
            config = self.get_ssh_config()
            
            # Remove host if it exists
            if host in config:
                del config[host]
                
                # Write updated config
                with open(config_path, "w") as f:
                    for host_name, settings in config.items():
                        f.write(f"Host {host_name}\n")
                        for key, value in settings.items():
                            f.write(f"    {key} {value}\n")
                        f.write("\n")
                        
                return True, f"Removed {host} from SSH config"
            else:
                return False, f"Host {host} not found in SSH config"
                
        except Exception as e:
            error_msg = f"Error removing host from SSH config: {e}"
            logger.error(error_msg)
            return False, error_msg 
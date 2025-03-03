"""Security-related functionality for SSH key management."""
import os
from pathlib import Path
from typing import Optional
import stat

from ..utils.logger import get_logger

logger = get_logger(__name__)

class KeySecurity:
    """Handles security-related operations for SSH keys."""

    def __init__(self):
        self.private_key_mode = 0o600  # -rw-------
        self.public_key_mode = 0o644   # -rw-r--r--
        self.dir_mode = 0o700          # drwx------

    def check_permissions(self, key_path: Path) -> bool:
        """Check if key file has correct permissions."""
        try:
            current_mode = stat.S_IMODE(os.stat(key_path).st_mode)
            expected_mode = (self.public_key_mode 
                           if key_path.suffix == '.pub' 
                           else self.private_key_mode)
            
            return current_mode == expected_mode
        except Exception as e:
            logger.error(f"Error checking permissions for {key_path}: {e}")
            return False

    def fix_permissions(self, key_path: Path) -> bool:
        """Set correct permissions for key files."""
        try:
            # Fix private key permissions
            if key_path.exists():
                os.chmod(key_path, self.private_key_mode)
            
            # Fix public key permissions if it exists
            pub_key = Path(f"{key_path}.pub")
            if pub_key.exists():
                os.chmod(pub_key, self.public_key_mode)
            
            # Fix SSH directory permissions
            ssh_dir = key_path.parent
            if ssh_dir.exists():
                os.chmod(ssh_dir, self.dir_mode)
                
            return True
        except Exception as e:
            logger.error(f"Error fixing permissions for {key_path}: {e}")
            return False

    def validate_key_name(self, name: str) -> bool:
        """Validate that a key name is safe and follows conventions."""
        # Check for path traversal attempts
        if ".." in name or "/" in name or "\\" in name:
            return False
            
        # Check for valid key name pattern
        valid_prefixes = ["id_ed25519", "id_rsa", "id_ecdsa", "id_dsa"]
        return any(name.startswith(prefix) for prefix in valid_prefixes)

    def secure_key_deletion(self, key_path: Path) -> bool:
        """Securely delete a key file by overwriting it before removal."""
        try:
            if not key_path.exists():
                return True
                
            # Overwrite file with random data
            size = key_path.stat().st_size
            with open(key_path, 'wb') as f:
                f.write(os.urandom(size))
                f.flush()
                os.fsync(f.fileno())
            
            # Remove the file
            key_path.unlink()
            
            # Remove public key if it exists
            pub_key = Path(f"{key_path}.pub")
            if pub_key.exists():
                pub_key.unlink()
                
            return True
        except Exception as e:
            logger.error(f"Error securely deleting {key_path}: {e}")
            return False

    def check_key_strength(self, key_path: Path) -> Optional[str]:
        """Check the strength and security of a key."""
        try:
            pub_key = Path(f"{key_path}.pub")
            if not pub_key.exists():
                return None
                
            content = pub_key.read_text()
            parts = content.strip().split()
            
            if len(parts) < 2:
                return "Invalid key format"
                
            key_type = parts[0]
            
            # Check key types and sizes
            if key_type == "ssh-rsa":
                return "RSA keys are being phased out, consider using Ed25519"
            elif key_type == "ssh-dss":
                return "DSA keys are deprecated and insecure"
            elif key_type == "ssh-ed25519":
                return None  # Ed25519 is currently recommended
            elif key_type.startswith("ecdsa"):
                return "ECDSA keys have potential security concerns"
                
            return None
        except Exception as e:
            logger.error(f"Error checking key strength for {key_path}: {e}")
            return "Error analyzing key" 
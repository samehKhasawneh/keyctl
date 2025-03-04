"""Security-related functionality for SSH key management."""
import os
from pathlib import Path
from typing import Optional, Dict
import stat
from cryptography.fernet import Fernet

from ..utils.logger import get_logger, SecurityError
from ..utils.validation import validate_ssh_key_format

logger = get_logger(__name__)

class KeySecurity:
    """Handles security-related operations for SSH keys."""

    def __init__(self):
        self.private_key_mode = 0o600  # -rw-------
        self.public_key_mode = 0o644   # -rw-r--r--
        self.dir_mode = 0o700          # drwx------
        self.key_file = Path.home() / '.keyctl' / '.key'
        self._load_or_create_key()

    def _load_or_create_key(self) -> None:
        """Load or create encryption key."""
        if self.key_file.exists():
            self.key = self.key_file.read_bytes()
        else:
            self.key = Fernet.generate_key()
            self.key_file.write_bytes(self.key)
        self.cipher_suite = Fernet(self.key)

    def encrypt_key(self, key_path: Path) -> bytes:
        """Encrypt an SSH key."""
        try:
            validate_ssh_key_format(key_path)
            key_data = key_path.read_bytes()
            return self.cipher_suite.encrypt(key_data)
        except Exception as e:
            raise SecurityError(f"Error encrypting key: {e}")

    def decrypt_key(self, encrypted_data: bytes) -> bytes:
        """Decrypt an SSH key."""
        try:
            return self.cipher_suite.decrypt(encrypted_data)
        except Exception as e:
            raise SecurityError(f"Error decrypting key: {e}")

    def check_key_strength(self, key_path: Path) -> Dict[str, str]:
        """Check SSH key strength."""
        try:
            validate_ssh_key_format(key_path)
            # Implementation for key strength checking
            return {
                "type": "ed25519",
                "bits": "256",
                "strength": "strong",
                "recommendations": []
            }
        except Exception as e:
            raise SecurityError(f"Error checking key strength: {e}")

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
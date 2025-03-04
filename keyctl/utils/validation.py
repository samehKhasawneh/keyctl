"""Input validation utilities for KeyCtl."""
import re
from pathlib import Path
from typing import Optional
from .logger import ValidationError

def validate_ssh_key_format(key_path: Path) -> bool:
    """Validate SSH key file format."""
    try:
        with open(key_path, 'r') as f:
            content = f.read().strip()
            if not content.startswith('-----BEGIN OPENSSH PRIVATE KEY-----'):
                raise ValidationError(f"Invalid SSH key format: {key_path}")
            if not content.endswith('-----END OPENSSH PRIVATE KEY-----'):
                raise ValidationError(f"Invalid SSH key format: {key_path}")
            return True
    except Exception as e:
        raise ValidationError(f"Error validating SSH key: {e}")

def validate_repository_url(url: str) -> bool:
    """Validate repository URL format."""
    patterns = [
        r'^git@[a-zA-Z0-9-]+\.com:[a-zA-Z0-9-]+/[a-zA-Z0-9-]+\.git$',
        r'^https://[a-zA-Z0-9-]+\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-]+\.git$'
    ]
    return any(re.match(pattern, url) for pattern in patterns)

def validate_host_pattern(host: str) -> bool:
    """Validate SSH host pattern."""
    pattern = r'^[a-zA-Z0-9-_.*]+$'
    return bool(re.match(pattern, host))

def validate_expiration_days(days: int) -> bool:
    """Validate key expiration days."""
    if not isinstance(days, int):
        raise ValidationError("Expiration days must be an integer")
    if days < 1:
        raise ValidationError("Expiration days must be positive")
    if days > 365:
        raise ValidationError("Expiration days cannot exceed 365")
    return True

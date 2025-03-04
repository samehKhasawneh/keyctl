"""Logging configuration for KeyCtl."""
import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
import os

def setup_logger(
    log_file: Optional[Path] = None,
    level: int = logging.INFO,
    max_size: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3
) -> None:
    """Set up logging configuration with rotation."""
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handler if log file is specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = handlers

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

# Custom exception classes
class KeyCtlError(Exception):
    """Base exception for KeyCtl errors."""
    pass

class ConfigError(KeyCtlError):
    """Configuration-related errors."""
    pass

class SecurityError(KeyCtlError):
    """Security-related errors."""
    pass

class ValidationError(KeyCtlError):
    """Validation-related errors."""
    pass

class OperationError(KeyCtlError):
    """Operation-related errors."""
    pass

# Initialize logger with environment-based level
log_level = os.getenv('KEYCTL_LOG_LEVEL', 'INFO')
setup_logger(
    log_file=Path.home() / '.keyctl' / 'keyctl.log',
    level=getattr(logging, log_level.upper())
) 
"""Logging configuration for KeyCtl."""
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    log_file: Optional[Path] = None,
    level: int = logging.INFO,
    format_string: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """Set up logging configuration."""
    # Create formatters
    file_formatter = logging.Formatter(format_string)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # File handler if log file is specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
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
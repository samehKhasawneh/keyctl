"""Logging configuration for KeyCtl."""
import logging
import sys
from pathlib import Path
from typing import Optional

def get_logger(name: str, log_file: Optional[Path] = None) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Only configure if not already configured
        logger.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        logger.addHandler(console_handler)
        
        # File handler (if log file specified)
        if log_file:
            try:
                # Ensure log directory exists
                log_file.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(file_formatter)
                file_handler.setLevel(logging.INFO)  # All logs to file
                logger.addHandler(file_handler)
            except Exception as e:
                logger.error(f"Failed to set up file logging: {e}")
        
        # Prevent propagation to root logger
        logger.propagate = False
    
    return logger 
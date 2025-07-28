"""
Logging configuration - Windows & Docker compatible
"""

import logging
import sys
from pathlib import Path

def setup_logger(name: str = None, level: str = 'INFO') -> logging.Logger:
    """Setup application logger with cross-platform path handling"""
    
    # Create logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler (always works)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with relative path
    try:
        # Use relative path that works in both environments
        if Path('/app').exists():
            # Docker environment
            log_dir = Path('/app/logs')
        else:
            # Local development environment
            log_dir = Path('./logs')
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / 'application.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.debug(f'Log file created at: {log_dir / "application.log"}')
        
    except Exception as e:
        # If file logging fails, continue with console only
        logger.warning(f'Could not setup file logging: {str(e)}')
        logger.info('Using console logging only')
    
    return logger

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.config.setting import settings

def setup_logger(name: str = "backend"):
    """Configure structured logging for the application"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        logs_dir / "backend.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
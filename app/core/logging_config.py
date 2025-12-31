import logging
import sys
from loguru import logger
from pathlib import Path

def setup_logging():
    # Remove default loguru sink
    logger.remove()
    
    # Console sink
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        backtrace=True,
        diagnose=True
    )
    
    # File sink
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "app.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        backtrace=True,
        diagnose=True
    )
    
    # Replace logging with loguru
    class LoguruHandler(logging.Handler):
        def emit(self, record):
            logger.log(record.levelno, record.getMessage())
    
    handler = LoguruHandler()
    logging.basicConfig(handlers=[handler], level=logging.INFO)
    
setup_logging()

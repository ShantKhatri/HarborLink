import logging
import os
import sys
from pathlib import Path

def setup_logging():
    """Configure logging for the application"""
    log_dir = Path(__file__).parents[3] / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "harborlink.log")
        ]
    )
    
    return logging.getLogger()

logger = setup_logging()
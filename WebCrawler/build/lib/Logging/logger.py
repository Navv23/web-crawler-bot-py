import logging
from Configs.settings import LOG_LEVEL
import os

def configure_logger():
    """
    Configures and returns a logger with the specified logging level.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    project_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(project_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'scraping.log')
    
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
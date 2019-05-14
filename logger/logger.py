import logging
from config.config import Config

config = Config()
config.parse()

logger = logging.getLogger('Application')
level = config.get('log_level')

logger.setLevel(level)
formatter = logging.Formatter('%(asctime)s : %(name)s - %(levelname)s : %(message)s')
sh = logging.StreamHandler()
sh.setLevel(level)
sh.setFormatter(formatter)
logger.addHandler(sh)
# fh = logging.FileHandler('logs/app.log')
# fh.setFormatter(formatter)
# logger.addHandler(fh)

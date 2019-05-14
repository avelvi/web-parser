from config.config import Config
from helpers.properties_validator import validate_properties
from parser.parser import Parser
from logger.logger import logger

config = Config()
config.parse()


def start():
	if validate_properties(config.get_properties()):
		logger.info('Starting application')
		scraper = Parser(config)
		scraper.run()
	else:
		logger.info('Something went wrong')


if __name__ == "__main__":
	start()

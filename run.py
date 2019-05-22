from config.config import Config
from helpers.properties_validator import validate_properties
from parsers.parser import Parser
from logger.logger import logger

config = Config()
config.parse()


def start():
	if validate_properties(config.get_properties()):
		logger.info('Starting application')
		parser = Parser(config)
		parser.run()
	else:
		logger.info('Something went wrong')


if __name__ == "__main__":
	start()

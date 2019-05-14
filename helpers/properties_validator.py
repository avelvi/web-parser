from voluptuous import Schema, Self, All, Range, Url, Email
from voluptuous.error import MultipleInvalid
from logger.logger import logger

TOTAL_MINUTES_IN_24_HOURS = 1440


def validate_properties(properties):
	try:
		main_schema(properties)
		logger.info('Properties JSON schema is valid')
		return True
	except MultipleInvalid as ex:
		logger.error(ex)
		return False


def validate_tag(tag):
	if not tag:
		return tag
	if tag.keys() == {'name', 'clazz', 'child_tag'}:
		return tag
	msg = 'Not a valid value for dictionary value'
	logger.error(msg)
	raise ValueError(msg)


def validate_time(time_str):
	try:
		splitted_time_str = time_str.split(":")
		hours = int(splitted_time_str[0])
		minutes = int(splitted_time_str[1])
	except (ValueError, IndexError):
		msg = "Please use the right format. The format should be in the 'hour:minutes'"
		logger.error(msg)
		raise ValueError(msg)
	if 0 <= hours < 24 and 0 <= minutes < 60:
		return time_str
	else:
		msg = "Hours should be between 0 and 23 inclusive. Minutes should be between 0 and 59 inclusive"
		logger.error(msg)
		raise ValueError(msg)


tag_schema = Schema({
	"name": str,
	"clazz": str,
	"child_tag": All(Self, validate_tag)
})

site_schema = Schema({
	'url': All(str, Url()),
	'interval': All(int, Range(min=1, max=TOTAL_MINUTES_IN_24_HOURS)),
	'start_time_notification': All(str, validate_time),
	'end_time_notification': All(str, validate_time),
	'tag': tag_schema,
	'keys': list
}, required=True)

main_schema = Schema({
	"timezone": str,
	"default_timezone": str,
	"log_level": str,
	"recipients": [
		All(str, Email)
	],
	"smtp": {
		"address": str,
		"port": int,
		"user": All(str, Email),
		"password": str
	},
	"sites": [
		site_schema
	]
}, required=True)

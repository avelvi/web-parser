import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from logger.logger import logger


class EmailNotification:

	def __init__(self, smtp_settings, recipients):
		self._smtp_settings = smtp_settings
		self._recipients = recipients

	def send_email(self, url, data):
		sender = self._smtp_settings['user']
		message = MIMEMultipart("alternative")
		message['Subject'] = f'Data from {url}'
		message['From'] = sender

		text_list = [f"Hi. There is a parsed result from {url}:\n"]
		html_list = [f"<html><body><p>Hi. There is a parsed result from {url}:</p><br/><ul>"]

		for d in data:
			text = d.get_text()
			href = d.get_href()
			text_list.append(f"{text} - {href}\n")
			html_list.append(f'<li><a href="{href}">{text}</a></li>')

		html_list.append("</ul><br/><body><html>")

		part1 = MIMEText(''.join(text_list), "plain")
		part2 = MIMEText(''.join(html_list), "html")

		message.attach(part1)
		message.attach(part2)

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self._smtp_settings['address'], self._smtp_settings['port'], context=context) as server:
			server.login(self._smtp_settings['user'], self._smtp_settings['password'])
			for recipient in self._recipients:
				server.sendmail(
					sender, recipient, message.as_string()
				)
				logger.info(f'Data was sent to {recipient}')


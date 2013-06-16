import smtplib, email, logging
from email.parser import Parser
from errors import EmailerError

import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

logger = logging.getLogger('emailer')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class Emailer(object):
	"""
	The core class that deals with sending emails.
	"""
	def __init__(self, sender=None, recipients=None, subject=None, msg=None):
		"""
		Instantiates a new emailer object.
		"""
		self.sender = sender
		if recipients is None:			
			recipients = []
		self.recipients = recipients

		self.subject = subject
		self.msg = msg
		self.smtp_server_settings = None

	def set_sender(self, sender):
		"""
		Sets the sender of the email. Performs email validation.
		"""
		if is_valid_email(sender):
			self.sender = sender
		else:
			raise EmailerError(msg="The provided sender email is not valid.")

	def set_recipients(self, recipients):
		"""
		Sets the recipients of the email. Performs email validation.
		"""
		for recipient in recipients:
			if is_valid_email(recipient):
				self.recipients.append(recipient) 
			else:
				raise EmailerError(msg="The provided recepient email: " + recipient + " is not valid.")

	def create_msg(self):
		"""
		Creates a message object.
		"""
		raise NotImplementedError("Subclasses must implement this method.")

	def _parse_headers(self):
		"""
		Parses RFC822 headers. Supposed to be a private method.
		"""
		header  = 'From: %s\n' % self.sender
		header += 'To: %s\n' % ','.join(self.recipients)
		header += 'Subject: %s\n\n' % self.subject
		return header

	def setup_smpt_server(self, smtp_server="smtp.gmail.com:587", username=None, password=None):
		"""
		Sets up the SMTP server settings.
		"""
		self.smtp_server_settings = dict(
			smtp_server = smtp_server,
			username  = username,
			password = password
		)

	def send_mail(self, one_by_one=False, logging=False):
		self._create_msg()
		msg = self._parse_headers() + self.msg.as_string()

		if self.smtp_server_settings:
			s = smtplib.SMTP(self.smtp_server_settings['smtp_server'])
		else:
			raise EmailerError("You have to setup the SMTP server using setup_smpt_server()")

		s.starttls()

		if self.smtp_server_settings['smtp_server'] == "smtp.gmail.com:587":
			username = self.smtp_server_settings['username']
			password = self.smtp_server_settings['password']
			s.login(username, password)

		if self.sender and len(self.recipients) != 0:
			if not one_by_one: 		
				logger.info('Sending email from %s' % self.sender)
				s.sendmail(self.sender, self.recipients, msg)
			else:
				for recipient in self.recipients:
					logger.info('Sending email from %s to %s' % (self.sender, recipient))
					s.sendmail(self.sender, [recipient], msg)
		else:
			raise EmailerError("Either recipient list is empty or no sender address has been specified.")
			
		s.quit()

class FileEmailer(Emailer):
	"""
	Sends emails using templates from files.
	"""
	def __init__(self, sender, recipients, subject, msg_file):
		super( FileEmailer, self ).__init__(sender, recipients, subject, None)
		self.msg_file = msg_file

	def _create_msg(self):
		"""
		Creates a message object.
		"""
		fp = open(self.msg_file, 'rb')
		self.msg = email.message_from_file(fp)
		fp.close()




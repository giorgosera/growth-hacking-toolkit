import smtplib, email, logging, re
from email.parser import Parser
from errors import EmailerError
import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

#Setup the logger
logger = logging.getLogger('emailer')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class Emailer(object):
	"""
	The core class that deals with sending emails.
	"""
	def __init__(self, template_file=None):
		"""
		Instantiates a new emailer object.
		"""
		self.sender = None
		self.recipient = None

		self.subject = None
		
		fp = open(template_file, 'rb')
		self.msg = email.message_from_file(fp)
		fp.close()
		
		self.smpt_server = None
		self.smtp_server_settings = None

	def set_subject(self, subject):
		"""
		Sets the subject of the email. 
		"""
		self.subject = subject
		if self.msg.has_key('Subject'):
			self.msg.replace_header('Subject', self.subject)
		else:
			self.msg['Subject'] = self.subject

	def set_sender(self, sender):
		"""
		Sets the sender of the email. Performs email validation.
		"""
		if is_valid_email(sender):
			self.sender = sender
			if self.msg.has_key('From'):
				self.msg.replace_header('From', self.sender)
			else:
				self.msg['From'] = self.sender
		else:
			raise EmailerError(msg="The provided sender email is not valid.")

	def set_recipient(self, recipient):
		"""
		Sets the recipient of the email. Performs email validation.
		"""
		if is_valid_email(recipient):
			self.recipient = recipient 
			if self.msg.has_key('To'):
				self.msg.replace_header('To', self.recipient)
			else:
				self.msg['To'] = self.recipient
		else:
			raise EmailerError(msg="The provided recepient email: " + recipient + " is not valid.")

	def setup_smpt_server(self, smtp_server="smtp.gmail.com:587", username=None, password=None):
		"""
		Sets up the SMTP server settings.
		"""
		self.smtp_server_settings = dict(
			smtp_server = smtp_server,
			username  = username,
			password = password
		)
	
	def send_mail(self, logging=False):

		self.smpt_server = smtplib.SMTP(self.smtp_server_settings['smtp_server'])
		self.smpt_server.starttls()
		try:
			username = self.smtp_server_settings['username']
			password = self.smtp_server_settings['password']
			self.smpt_server.login(username, password)
		except smtplib.SMTPAuthenticationError:
			raise EmailerError(msg="SMTP authentication failed.")

		if self.sender and self.recipient:
			logger.info('Sending email from %s to %s' % (self.sender, self.recipient))
			#self.smpt_server.sendmail(self.sender, self.recipient, self.msg.as_string())
		else:
			raise EmailerError("Either recipient or sender address has not been specified.")
			
		self.smpt_server.quit()

		

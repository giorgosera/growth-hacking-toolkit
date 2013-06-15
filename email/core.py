import smtplib, email, getpass
from email.parser import Parser
from errors import EmailerError

import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

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

	def send_mail(self, smtpserver="smtp.gmail.com:587"):
		self._create_msg()
		msg = self._parse_headers() + self.msg.as_string()  
		s = smtplib.SMTP(smtpserver)
		s.starttls()
		if smtpserver == "smtp.gmail.com:587":
			username = raw_input('Enter username: ')
			password = getpass.getpass("Enter password: ")
			s.login(username, password)
		if self.sender and len(self.recipients) != 0: 	
			s.sendmail(self.sender, self.recipients, msg)
		else:
			raise EmailerError("Either recipient list is empty or no sender address has been specified.")
			
		s.quit()

class FileEmailer(Emailer):
	"""
	Sends emails using file templates.
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




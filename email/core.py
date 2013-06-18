import smtplib, email, logging, re, csv
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
formatter = logging.Formatter('[%(name)-2s: %(levelname)-1s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Emailer(object):
	"""
	The core class that deals with sending emails.
	"""
	def __init__(self, template_file):
		"""
		Instantiates a new emailer object.
		"""
		self.sender = None
		self.recipient = None
		self.subject = None
		self.smpt_server = None
		self.smtp_server_settings = None
		self.template_file = template_file

	def construct_msg(self):
		"""
		Sets the msg of the email. 
		"""
		fp = open(self.template_file, 'rb')
		self.msg = email.message_from_file(fp)
		fp.close()
		self.msg['Subject'] = self.subject
		self.msg['From'] = self.sender
		self.msg['To'] = self.recipient

	def set_subject(self, subject):
		"""
		Sets the subject of the email. 
		"""
		self.subject = subject

	def set_sender(self, sender):
		"""
		Sets the sender of the email. Performs email validation.
		"""
		if is_valid_email(sender):
			self.sender = sender
		else:
			raise EmailerError(msg="The provided sender email is not valid.")

	def set_recipient(self, recipient):
		"""
		Sets the recipient of the email. Performs email validation.
		"""
		if is_valid_email(recipient):
			self.recipient = recipient 
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
	
	def send_mail(self):

		self.smpt_server = smtplib.SMTP(self.smtp_server_settings['smtp_server'])
		self.smpt_server.starttls()
		try:
			username = self.smtp_server_settings['username']
			password = self.smtp_server_settings['password']
			self.smpt_server.login(username, password)
		except smtplib.SMTPAuthenticationError:
			raise EmailerError(msg="SMTP authentication failed.")

		if self.sender and self.recipient:
			self.smpt_server.sendmail(self.sender, self.recipient, self.msg.as_string())
			logger.info('Sent email from %s to %s' % (self.sender, self.recipient))
		else:
			raise EmailerError("Either recipient or sender address has not been specified.")
			
		self.smpt_server.quit()


class PersonalisedEmailer(Emailer):
	"""
	Sends personalised emails using templates from files and data loaded from csv.
	"""
	def __init__(self, csv_file=None, template_file=None):
		super( PersonalisedEmailer, self ).__init__(template_file)
		self.rules_dict = None
		self.csv_file = csv_file
		self.regex = re.compile('(\\*\\|)((?:[a-z][a-z0-9_]*))(\\|\\*)',re.IGNORECASE|re.DOTALL)
		self.assisted = False

	def personalise(self, entry):
		"""
		Parses a text file replacing placeholders with the data from the csv according to
		the specified rules.
		"""		
		logger.info("Personalising email for %s" % entry['Email'])
		def repl(m):
			rule_value = self.rules_dict[m.group(2)]

			if rule_value:
				placeholder_value = entry[rule_value]

				#If assisted is selected the user will review the placeholder values
				if self.assisted:
					c = None
					while (c  not in ['Y', 'N']):
						c = raw_input(" > Replace placeholder %s with '%s'? [Y/N]: " % (m.group(1) + m.group(2) +m.group(3), entry[rule_value]))
					if c == 'N':
						placeholder_value = raw_input(" > Type the correct value for placeholder %s : " % (m.group(1) + m.group(2) +m.group(3)))
			else:
				placeholder_value = raw_input(" > Type the correct value for placeholder %s : " % (m.group(1) + m.group(2) +m.group(3)))
			return placeholder_value

		self.msg.set_payload(re.sub(self.regex, repl, self.msg.get_payload()))

	def send_mail(self, assisted=False):
		self.assisted = assisted
		f = open(self.csv_file, 'rb') 
		try:
			reader = csv.reader(f)  
			header = None
			for i, row in enumerate(reader):   
				if i == 0:
					header = row
				else:
					entry = {key: row[j] for j, key in enumerate(header)}
					try:
						self.set_recipient(entry['Email']) 
					except KeyError, e:
						raise EmailerError("The CSV file must contain a column of email addresses.")
					self.construct_msg()
					self.personalise(entry)
					if self.assisted:
						print "======================================="
						logger.info(self.msg)
						print "======================================="
						c = None
						while (c  not in ['Y', 'N']):		
							c = raw_input(" > Is it OK to send? [Y/N]")
						if c == 'N':
							logger.info("Skipping email to %s" % entry['Email'])
							continue
					try:
						super(PersonalisedEmailer, self).send_mail()
					except EmailerError, e:
						print str(e.msg)					
		finally:
			f.close()     

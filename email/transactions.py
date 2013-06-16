import getpass
from core import FileEmailer
from errors import EmailerError

class NewsletterSender(object):
	"""
	Sends mass email newsletters
	"""
	def __init__(self, recipient_list=None, subject=None, template_file=None):
		"""
		Constructs an new NewsletterSender object.
		"""
		if recipient_list is None:
			recipient_list = []
		self.recipient_list = recipient_list

		self.subject = subject
		self.template_file = template_file
		self.emailer = FileEmailer("basketballcy@gmail.com", self.recipient_list, self.subject, self.template_file)

	def send(self, logging=False):

		#Setup SMPT
		username = raw_input("Enter your Gmail username: ")			
		password = getpass.getpass("Enter your Gmail password: ")			
		self.emailer.setup_smpt_server("smtp.gmail.com:587", username, password)
		
		try:
			self.emailer.send_mail(one_by_one=True, logging=logging)
		except EmailerError, e:
			print str(e.msg)








from core import FileEmailer

class NewsletterSender(object):
	"""
	Sends mass email newsletters
	"""
	def __init__(self, email_list=None, template_file=None):
		"""
		Constructs an new NewsletterSender object.
		"""
		if email_list is None:
			email_list = []
		self.email_list = email_list

		self.template_file = template_file
		self.emailer = FileEmailer("basketballcy@gmail.com", email_list, "Hello", "/home/george/akka.txt")

	def send(self):
		try:
			self.emailer.send_mail()
		except EmailerError, e:
			print str(e)








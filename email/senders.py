import csv, re
from core import Emailer
from errors import EmailerError

class PersonalisedSender(object):
	"""
	Sends personalised emails using templates from files and data loaded from csv.
	"""
	def __init__(self, csv_file=None, template_file=None):
		self.rules_dict = None
		self.csv_file = csv_file
		self.regex = re.compile('(\\*\\|)((?:[a-z][a-z0-9_]*))(\\|\\*)',re.IGNORECASE|re.DOTALL)
		self.emailer = Emailer(template_file=template_file)

	def personalise(self, entry):
		"""
		Parses a text file replacing placeholders with the data from the csv according to
		the specified rules.
		"""
		def repl(m):
			rule_value = self.rules_dict[m.group(2)]
			return entry[rule_value]

		self.emailer.msg.set_payload(re.sub(self.regex, repl, self.emailer.msg.get_payload()))
		print self.emailer.msg.get_payload()

	def send(self):
		"""
		Sends personalised emails to the recipients specified in the csv.
		"""
		f = open(self.csv_file, 'rb') 
		try:
			reader = csv.reader(f)  
			header = None
			for i, row in enumerate(reader):   
				if i == 0:
					header = row
				else:
					entry = {key: row[j] for j, key in enumerate(header)}
					self.personalise(entry) 
					try:
						self.emailer.set_recipient(entry['Email'])
						self.emailer.send_mail(logging=True)
					except EmailerError, e:
						print str(e.msg)					
		finally:
			f.close()     

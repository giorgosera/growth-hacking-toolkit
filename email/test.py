import getpass
from core import PersonalisedEmailer

email_subject = "Want to monetize your app with real rewards?"
email_template_file = "/home/george/akka.txt"
leads_csv_file = "/home/george/leads.csv"

sender = PersonalisedEmailer(csv_file=leads_csv_file, template_file=email_template_file)
sender.rules_dict = {
	"DEVELOPER": "First Name",
	"APP_NAME": "App Name",
	"DAY": None		
}
sender.set_subject(email_subject)
sender.set_sender("george@avocarrot.com")
username = raw_input("Enter Gmail username: ") 
password = getpass.getpass("Enter Gmail password: ")
sender.setup_smpt_server("smtp.gmail.com:587", username, password)
sender.send_mail(assisted=True)
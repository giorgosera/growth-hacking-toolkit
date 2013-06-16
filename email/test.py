from senders import PersonalisedSender

email_subject = "Hello World"
email_template_file = "/home/george/akka.txt"
leads_csv_file = "/home/george/leads.csv"

sender = PersonalisedSender(csv_file=leads_csv_file, template_file=email_template_file)
sender.rules_dict = {
	"DEVELOPER": "First Name",
	"APP_NAME": "App Name"		
}
sender.emailer.set_subject(email_subject)
sender.emailer.set_sender("giorgosera@gmail.com")
sender.emailer.setup_smpt_server("smtp.gmail.com:587", "giorgosera@gmail.com", "GIOimp1903")
sender.send()

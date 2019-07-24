import smtplib
import json
from datetime import datetime

with open('config.json') as json_file:
   config = json.load(json_file)
   SERVER = config["SERVER"]
   PORT = config["PORT"]
   BOT_EMAIL = config["BOT_EMAIL"]
   BOT_PASSWORD = config["BOT_PASSWORD"]
   HUMAN_EMAIL = config["HUMAN_EMAIL"]

def send_email(subject, message):
   # Start SMTP server
   server = smtplib.SMTP_SSL(SERVER,port=PORT)
   server.ehlo()
   server.login(BOT_EMAIL, BOT_PASSWORD)

   dt = datetime.today()

   # Send email
   email_text = "Subject: {} {}\n\n{}".format(subject, dt.strftime("%m-%d"), message)
   server.sendmail(BOT_EMAIL, HUMAN_EMAIL, email_text)

   print("\n\n###################################\n")
   print(email_text)
   print()

   # Stop SMTP Server
   server.quit()

import smtplib
import json
from datetime import datetime

with open('config.json') as json_file:
   config = json.load(json_file)
   ENABLE_EMAILS = config["ENABLE_EMAILS"]
   
   if ENABLE_EMAILS:
      SERVER = config["SERVER"]
      PORT = config["PORT"]
      BOT_EMAIL = config["BOT_EMAIL"]
      BOT_PASSWORD = config["BOT_PASSWORD"]
      HUMAN_EMAIL = config["HUMAN_EMAIL"]


def send_email(subject, message):
   dt = datetime.today()
   email_text = "Subject: {} {}\n\n{}".format(subject, dt.strftime("%m-%d"), message)

   if ENABLE_EMAILS:
      server = smtplib.SMTP_SSL(SERVER,port=PORT)
      server.ehlo()
      server.login(BOT_EMAIL, BOT_PASSWORD)
      server.sendmail(BOT_EMAIL, HUMAN_EMAIL, email_text)
      server.quit()

   print("\n\n###################################\n")
   print(email_text)
   print()

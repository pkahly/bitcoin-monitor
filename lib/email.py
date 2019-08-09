import smtplib
from datetime import datetime
from lib import config_reader


def send_email(subject, message):
   config = config_reader.get_config()
   dt = datetime.today()
   
   if config.use_testnet:
      subject = "[TESTNET] " + subject
   elif config.use_regtest:
      subject = "[REGTEST] " + subject
   
   email_text = "Subject: {} {}\n\n{}".format(subject, dt.strftime("%m-%d"), message)

   if config.enable_emails:
      server = smtplib.SMTP_SSL(config.server, port=config.port)
      server.ehlo()
      server.login(config.bot_email, config.bot_password)
      server.sendmail(config.bot_email, config.human_email, email_text)
      server.quit()

   print("\n\n###################################\n")
   print(email_text)
   print()

import smtplib
from datetime import datetime


def send_email(config, subject, message):
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

   logging.info("\n\n###################################\n")
   logging.info(email_text)
   logging.info("\n")

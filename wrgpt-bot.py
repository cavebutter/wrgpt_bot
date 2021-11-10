import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import sys
import logging
import argparse


#  Environment Stuff
load_dotenv()
user = os.getenv("user")
password = os.getenv("password")
mailserver = os.getenv("mailserver")
port = os.getenv("port")
id = os.getenv("id")
#dealer = os.getenv("dealer")
test_recipient = 'cavebutter@gmail.com'


#  Other variables
#  TODO apply string methods for yes/no input so that it's case insensitive
subject = "id="+id
money_plays = ['bet', 'call', 'make', 'raise']
any = ['*', 'any']
yesno = ['yes', 'no', "y", 'n', 'Yes', 'No', 'YES', 'NO']

# Logging
logging.basicConfig(filename='wrgpt.log', filemode='a', format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

#  Args
#  TODO add sticky flag -s
#  TODO add some housekeeping arguments e.g. WHAT, JUSTME, etc.
parser = argparse.ArgumentParser(description="Automate wrgpt poker actions")
parser.add_argument('play', metavar='Play', type=str.lower, choices=['bet', 'call', 'fold', 'make', 'raise', 'pot', 'jam', 'undo'], help="What is your play?")
parser.add_argument("amount", metavar="Amount", nargs='?', help="How much?", type=int, default=1)
args = parser.parse_args()
logging.debug('Parsed arguments')

#######  PLAYS AND AMOUNTS  ######

#  CASE money_play AND usable amount
#  TODO more graceful exception handling of non-int amount
#  Passed test
if args.play in money_plays and args.amount > 1:
    message = args.play.upper() + " $" + str(args.amount)
    logging.debug(f'Play is {args.play} and amount is greater than 1: {args.amount}')
    logging.info(f'{message}')


#  CASE money_play AND amount == 1, confirm intent
#  Passed test
elif args.play in money_plays and args.amount == 1:
    decision = ''
    logging.debug(f'Money Play ({args.play}) with no amount.')
    while decision not in yesno:
        decision = input(f'Do you mean to {args.play} any amount?')
        if decision in ['yes', 'y', 'YES', 'Yes']:
            amount = "*"
            message = args.play.upper() + ' ' + amount
            logging.debug(f"Confirmed 'any' amount.  Amount = {amount}")
            logging.info(message)
        elif decision in ['no', 'n', 'NO', 'No']:
            print("That's just not going to work out.  Please start again")
            logging.info("Data Entry Error.  Quitting")
            sys.exit()

#  CASE not a money play
elif args.play not in money_plays:
    message = args.play.upper()
    logging.info(f"Non money play: {args.play}.  Message = {message}")

######  EMAIL  #######

mail = MIMEMultipart()
mail["Subject"] = subject
mail["From"] = user
mail["To"] = test_recipient
mail.attach(MIMEText(message, "plain"))

#  Try to connect to mailserver and send
context = ssl.create_default_context()
with smtplib.SMTP_SSL(mailserver, port, context=context) as server:
    server.login(user, password)
    server.sendmail(user, test_recipient, mail.as_string())

#  TODO Add a summary notification to stdout via print with confirmation of amount and successful send
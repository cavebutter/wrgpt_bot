from imap_tools import MailBox
import re
import subprocess as s

class Mail:
    def __init__(self, uid, subject, from_, date_str, date, text):
        self.uid = uid
        self.subject = subject
        self.from_ = from_
        self.date_str = date_str
        self.date = date
        self.text = text


class Account():
    def __init__(self, server, email, password):
        self.server = server
        self.email = email
        self.password = password

    def login(self):
        """Login to server account, return mailbox object"""
        mb = MailBox(self.server).login(self.email, self.password)
        return mb


def fetch_most_recent(imap_server, user, password, folder="INBOX.Poker"):
    """Fetch the most recent message in the specified folder and return it as Mail"""
    with Account(imap_server, user, password).login() as login:
        login.folder.set(folder)
        newest = 1
        for msg in login.fetch():
            if newest == 1:
                newest = Mail(msg.uid, msg.subject, msg.from_, msg.date_str, msg.date, msg.text)
            elif msg.date > newest.date:
                newest = Mail(msg.uid, msg.subject, msg.from_, msg.date_str, msg.date, msg.text)
    return newest


def get_table_url(recent_message):
    """Extract the table URL from a Mail object"""
    pattern = r'[(http://hands.)|\w]*?[\w]*\.[-/\w]*\.\w*[(/{1})]?[#-\./\w]*[(/{1,})]?'
    msg = recent_message.text
    table_url = re.search(pattern,msg)
    return table_url.group()


def display_webpage(url):
    """Display the passed url in terminal using w3m"""
    cmd = ['w3m', url]
    s.run(cmd)


def display_status(imap_server, user, password, folder="INBOX.Poker"):
    """All three of the above functions chained for convenience"""
    foo = fetch_most_recent(imap_server, user, password)
    bar = get_table_url(foo)
    display_webpage(bar)

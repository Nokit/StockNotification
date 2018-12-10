import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import sys
import argparse



def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, password, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

parser = argparse.ArgumentParser()
parser.add_argument('fromaddr', help='please set the sender\'s address', type=str)
parser.add_argument('pwd', help='please set the password of sender\'s address', type=str)
parser.add_argument('toaddr', help='please set the receiver\'s address', type=str)
parser.add_argument('title', help='please set title of the message', type=str)
parser.add_argument('msg', help='please set the message body', type=str)

args = parser.parse_args()

if __name__ == '__main__':
    if sys.argv:
        del sys.argv[1:]
    msg = create_message(args.fromaddr, args.toaddr, args.title, args.msg)
    send(args.fromaddr, args.pwd, args.toaddr, msg)

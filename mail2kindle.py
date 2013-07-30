#!/usr/bin/python
# -*- coding: utf-8 -*-

your_addr = '@gmail.com'
your_pass = ''
kindle_addr = '@kindle.com'

import os, sys
import smtplib
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.Utils import formatdate

def create_message(from_addr, to_addr, fpath):
    fname = os.path.basename(fpath)
    subject = fname
    body = fname
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    msg.attach(MIMEText(body))
    mobi = open(fpath).read()
    att = MIMEApplication(mobi, "x-mobipocket-ebook")
    att.add_header("Content-Disposition","attachment", filename=fname)
    msg.attach(att)

    return msg

def send_via_gmail(from_addr, to_addr, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(your_addr, your_pass)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "No file path"
        exit()
    fpath = sys.argv[1]
    if not os.path.exists(fpath):
        print "No exists file"
        exit()
    from_addr = your_addr
    to_addr = kindle_addr
    
    msg = create_message(from_addr, to_addr, fpath)
    send_via_gmail(from_addr, to_addr, msg)


"""
Created on 4 December 2016

@author: Christian Sisti

Given a list of Name -> emails it send email to each of the participants
of the Secret Santa telling the person to buy the gift.
"""

import csv
import copy
import random
import smtplib

from email.mime.text import MIMEText
from string import Template


EMAIL_FROM = ''
EMAIL_SUBJECT = 'SECRET SANTA DRAW RESULT'
EMAIL_CONTENT_TEMPLATE = Template(
    """
    Ciao $secret_santa_name,

    The Secret Santa draw is done!

    Your assigned super-secret gift receiver is: $gift_receiver

    =====

    Keep it secret! This email is self generated, no one knows this except you.

    The code is open sourced here: https://github.com/ciscox83/secretsanta

    """
)


santas = {}
receivers = {}
associations = {}


def main():

    load_data()
    draw_names()
    send_emails()


def load_data():
    with open('Santas.csv', 'r') as santas_csv:
        reader = csv.reader(santas_csv, delimiter='|')
        for row in reader:
            name = row[0].strip()
            email = row[1].strip()
            santas[name] = email
            receivers[name] = email


def draw_names():
    for santa_name in santas:
        receiver_name = pick_random_receiver_for(santa_name)
        associations[santa_name] = receiver_name


def pick_random_receiver_for(name):
    fail_on_corner_case(name)
    receivers_copy = copy.deepcopy(receivers)
    if name in receivers_copy.keys():
        del receivers_copy[name]
    draw = random.choice(receivers_copy.keys())
    if draw in receivers.keys():
        del receivers[draw]
    return draw


def fail_on_corner_case(name):
    if len(receivers) == 1:
        last_one = receivers.keys()[0]
        if last_one == name:
            print("Very very unlucky, trying again.")
            exit()


def send_emails():
    for association in associations:

        email_to = santas[association]
        email_content = EMAIL_CONTENT_TEMPLATE.substitute(
            to=email_to,
            secret_santa_name=association,
            gift_receiver=associations[association])

        msg = MIMEText(email_content)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = email_to

        try:
            mail_server
            mail_server.sendmail(EMAIL_FROM, [email_to], msg.as_string())
            mail_server.quit()
        except NameError:
            print """
                    ERROR: You need to define the  MAIL_SERVER variable pointing to your mail server:
                    e.g., smtplib.SMTP('localhost')
                """
            exit()

if __name__ == "__main__":
    main()

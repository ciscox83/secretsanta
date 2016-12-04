"""
Created on 4 December 2016

@author: Christian Sisti

Given a list of Name -> emails it send email to each of the participants
of the Secret Santa telling the person to buy the gift.
"""

import csv
import copy
import random

from email.mime.text import MIMEText
from string import Template


EMAIL_FROM = 'secret_santa@noreply.com'
EMAIL_SUBJECT = 'SECRET SANTA DRAW RESULT'
EMAIL_CONTENT = Template(
    """Ciao $secret_santa_name, send a gift to $gift_receiver"""
)


santas = {}
receivers = {}
associations = {}

try:
    MAIL_SERVER
except NameError:
    print "ERROR: You need to define the  MAIL_SERVER variable pointing to your mail server"
    exit()


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
        print EMAIL_CONTENT.substitute(to=email_to, secret_santa_name=association, gift_receiver=associations[association])

        msg = MIMEText(EMAIL_CONTENT)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = email_to

        MAIL_SERVER.sendmail(EMAIL_FROM, [email_to], msg.as_string())
        MAIL_SERVER.quit()

if __name__ == "__main__":
    main()

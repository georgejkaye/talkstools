#!/usr/bin/python3

import json
from scraper import get_next_talk
from emails import write_email, send_email
import datetime
import sys

# Modes
ANNOUNCE = 0
REMINDER = 1


def find_talk_and_send_email(config, mode):

    if mode == ANNOUNCE:
        range = 5
        template = "announce.txt"
    elif mode == REMINDER:
        range = 1
        template = "reminder.txt"

    next_talk = get_next_talk(config, range)

    if next_talk is not None:
        email = write_email(config, template, next_talk)
        send_email(config, next_talk, email)


def main(config_file):

    with open(config_file) as config_stream:
        config = json.load(config_stream)

    today = datetime.datetime.today()

    if today.weekday() == int(config["day"]):
        mode = REMINDER
        time = config["reminder_time"]
    elif today.weekday() == 0:
        mode = ANNOUNCE
        time = config["announce_time"]
    else:
        print("Not the right day to send an email")
        exit(1)

    if today.time() == datetime.datetime.strptime(time, "%H:%M"):
        find_talk_and_send_email(config, mode)
    else:
        print("Not the right time to send an email")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config file>")
        exit(1)
    main(sys.argv[1])

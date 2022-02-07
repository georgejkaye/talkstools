#!/usr/bin/python3

import json
from scraper import get_next_talk
from emails import write_email, send_email
from debug import debug
import datetime
import sys

# Modes
ANNOUNCE = 0
REMINDER = 1


def find_talk_and_send_email(config, log_file, mode):

    if mode == ANNOUNCE:
        range = 5
        template = "announce.txt"
    elif mode == REMINDER:
        range = 1
        template = "reminder.txt"

    next_talk = get_next_talk(config, log_file, range)

    if next_talk is not None:
        email = write_email(config, template, next_talk)
        send_email(config, log_file, next_talk, email)


def main(config_file, log_file):

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
        debug(log_file, "Not the right day to send an email")
        exit(1)

    if today.time() == datetime.datetime.strptime(time, "%H:%M"):
        find_talk_and_send_email(config, log_file, mode)
    else:
        debug(log_file, "Not the right time to send an email")
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

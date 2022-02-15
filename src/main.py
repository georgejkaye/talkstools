#!/usr/bin/python3

from config import load_config, ANNOUNCE, REMINDER, ABSTRACT
from scraper import get_next_talk
from emails import write_email, send_email
from debug import debug
import datetime
import sys


def find_talk_and_send_email(config, mode):

    if mode == ANNOUNCE:
        range = 5
        template = "announce.txt"
    elif mode == REMINDER:
        range = config.reminder.offset + 1
        template = "reminder.txt"

    next_talk = get_next_talk(config, range)

    if next_talk is not None:
        email = write_email(config, template, next_talk)
        send_email(config, next_talk, email, mode)


def main(config_file, log_file):

    today = datetime.datetime.today()

    config = load_config(config_file, log_file)

    if today.weekday() == int(config["day"]):
        mode = REMINDER
        time = config["reminder_time"]
    elif today.weekday() == 0:
        mode = ANNOUNCE
        time = config["announce_time"]
    elif today.weekday() == 4:
        mode = ABSTRACT
        time = config["abstract_time"]
    else:
        debug(config.log, "Not the right day to send an email")
        exit(1)
    # Parse the time from the config
    time = datetime.datetime.strptime(time, "%H:%M")
    # We can't be too precise as it might take a few seconds to load the script
    if today.hour == time.hour and today.min == time.min:
        find_talk_and_send_email(config, mode)
    else:
        debug(config.log, "Not the right time to send an email")
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

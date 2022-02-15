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


def check_config(config):
    if "talks_id" not in config:
        return "talks_id"

    if "smtp" in config:
        smtp = config["smtp"]
        if "port" not in smtp:
            return "smtp.port"
        if "host" not in smtp:
            return "smtp.host"
        if "user" not in smtp:
            return "smtp.user"
        if "password" not in smtp:
            return "smtp.password"
    else:
        return "smtp"

    if "sender_email" not in config:
        return "sender_email"
    if "recipient_email" not in config:
        return "recipient_email"

    if "zoom" in config:
        zoom = config["zoom"]
        if "link" not in zoom:
            return "zoom.link"
        if "id" not in zoom:
            return "zoom.id"
        if "password" not in zoom:
            return "zoom.password"
    else:
        return "zoom"

    if "room" not in config:
        return "room"

    if "admin" in config:
        admin = config["admin"]
        if "name" not in admin:
            return "admin.name"
        if "email" not in admin:
            return "admin.email"
    else:
        return "admin"

    if "announce_time" not in config:
        return "announce_time"
    if "reminder_time" not in config:
        return "reminder_time"

    return ""


def load_config(config_file):
    with open(config_file) as config_stream:
        config = json.load(config_stream)
    check = check_config(config)
    if not check == "":
        debug(log_file, f"Incomplete config, missing field {error}")
        exit(1)
    return config


def main(config_file, log_file):

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
    # Parse the time from the config
    time = datetime.datetime.strptime(time, "%H:%M")
    # We can't be too precise as it might take a few seconds to load the script
    if today.hour == time.hour and today.min == time.min:
        find_talk_and_send_email(config, log_file, mode)
    else:
        debug(log_file, "Not the right time to send an email")
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

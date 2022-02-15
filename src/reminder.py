#!/bin/python3

import sys

from main import find_talk_and_send_email, REMINDER, load_config


def main(config_file, log_file):
    config = load_config(config_file, log_file)
    find_talk_and_send_email(config, REMINDER)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reminder.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

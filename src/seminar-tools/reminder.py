#!/bin/python3

import sys

from config import load_config
from tasks import reminder_seminar
from scraper import get_next_talk


def main(config_file, log_file, stdout):
    config = load_config(config_file, log_file)
    for seminar in config.seminars:
        next_talk = get_next_talk(config, seminar)
        if next_talk is not None:
            reminder_seminar(config, seminar, next_talk, stdout)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python reminder.py <config file> <log file>")
        exit(1)
    stdout = len(sys.argv) == 4 and sys.argv[3] == "--stdout"
    main(sys.argv[1], sys.argv[2], stdout)

#!/bin/python3

import sys

from config import load_config
from main import find_talk_and_send_email, ANNOUNCE


def main(config_file, log_file):
    config = load_config(config_file, log_file)
    for seminar in config.seminars:
        find_talk_and_send_email(config, seminar, ANNOUNCE)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python announce.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

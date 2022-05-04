#!/bin/python3

import sys

from config import load_config, GENERATE
from main import find_talk_and_send_email


def main(config_file, log_file):
    config = load_config(config_file, log_file)
    for seminar in config.seminars:
        find_talk_and_send_email(config, seminar, GENERATE)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <config file> <log file>")
        exit(1)
    if len(sys.argv) == 3:
        log = sys.argv[2]
    else:
        log = None

    main(sys.argv[1], log)

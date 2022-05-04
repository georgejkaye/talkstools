#!/usr/bin/python3

from config import load_config
from tasks import check_for_tasks
import sys


def main(config_file, log_file):
    config = load_config(config_file, log_file)
    check_for_tasks(config)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

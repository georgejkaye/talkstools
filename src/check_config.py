import sys


def main(config_file, log_file):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python announce.py <config file> <log file>")
        exit(1)
    main(sys.argv[1], sys.argv[2])

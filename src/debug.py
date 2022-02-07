import datetime


def debug(log_file, string):
    with open(log_file, "a+") as log:
        now = datetime.datetime.now()
        timestring = now.strftime("%d-%m-%y %H:%M:%S")
        log.write(f"[{timestring}] {string}\n")

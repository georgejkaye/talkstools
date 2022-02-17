import datetime


def debug(config, string):
    with open(config.log, "a+") as log:
        now = datetime.datetime.now()
        timestring = now.strftime("%d-%m-%y %H:%M:%S")
        log.write(f"[{timestring}] {string}\n")

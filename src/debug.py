import datetime


def debug(config, string):
    if isinstance(config, str):
        log = config
    else:
        log = config.log

    with open(log, "a+") as log:
        now = datetime.datetime.now()
        timestring = now.strftime("%d-%m-%y %H:%M:%S")
        log.write(f"[{timestring}] {string}\n")

import datetime


def debug(config, string):
    if config is not None:
        if isinstance(config, str):
            log = config
        else:
            if config.log is not None:
                log = config.log
            else:
                return

        with open(log, "a+") as log:
            now = datetime.datetime.now()
            timestring = now.strftime("%d-%m-%y %H:%M:%S")
            log.write(f"[{timestring}] {string}\n")

import yaml
from debug import debug
from scraper import get_talks_page
import calendar

# Modes
ANNOUNCE = 0
REMINDER = 1
ABSTRACT = 2


class ZoomDetails:
    def __init__(self, yaml):
        self.link = yaml["link"]
        self.id = yaml["id"]
        self.password = yaml["password"]


class AdminDetails:
    def __init__(self, yaml):
        self.name = yaml["name"]
        self.email = yaml["email"]


class SMTPDetails:
    def __init__(self, yaml):
        self.host = yaml["host"]
        self.port = yaml["port"]
        self.user = yaml["user"]
        self.password = yaml["password"]


class Daytime:
    def __init__(self, day, time, offset=0):
        self.day = day
        self.time = time
        self.days_before = offset


def get_offset_day(day, offset):
    day = day - offset
    if day < 0:
        day = day + 5
    return day


def get_daytime_from_offset(yaml, default_offset, default_time, origin):
    if yaml is None:
        offset = default_offset
        time = default_time
    else:
        if "days_before" in yaml:
            offset = yaml["days_before"]
        else:
            offset = default_offset
        if "time" in yaml:
            time = yaml["time"]
        else:
            time = default_time
    day = get_offset_day(origin, offset)
    return Daytime(day, time, offset)


def get_daytime(yaml, default_day, default_time):
    if yaml is None:
        day = default_day
        time = default_time
    else:
        if "day" in yaml:
            day = yaml["day"]
        else:
            day = default_day
        if "time" in yaml:
            time = yaml["time"]
        else:
            time = default_time
    return Daytime(day, time)


default_announce_offset = 2
default_announce_time = "10:00"
default_reminder_offset = 0
default_reminder_time = "10:00"
default_abstract_offset = 1
default_abstract_time = "10:00"


class Config:
    def __init__(self, yaml, log_file):
        self.id = yaml["talks_id"]
        self.page = get_talks_page(self.id)
        self.smtp = SMTPDetails(yaml["smtp"])
        self.sender_email = yaml["sender_email"]
        self.recipient_email = yaml["recipient_email"]
        self.zoom = ZoomDetails(yaml["zoom"])
        self.room = yaml["room"]
        self.admin = AdminDetails(yaml["admin"])
        self.talk_day = yaml["talk_day"]
        self.talk_day_name = calendar.day_name[self.talk_day]
        self.discord = yaml["discord"]

        self.announce = get_daytime_from_offset(
            yaml.get("announce"), default_announce_offset, default_announce_time, self.talk_day)
        self.reminder = get_daytime_from_offset(
            yaml.get("reminder"), default_reminder_offset, default_reminder_time, self.talk_day)
        self.abstract = get_daytime_from_offset(yaml.get(
            "abstract"), default_abstract_offset, default_abstract_time, self.announce.day)

        if "emails" in yaml:
            self.emails = yaml["emails"]

        self.log = log_file


def check_config(config):
    if "talks_id" not in config:
        return "talks_id"

    if "smtp" in config:
        smtp = config["smtp"]
        if "port" not in smtp:
            return "smtp.port"
        if "host" not in smtp:
            return "smtp.host"
        if "user" not in smtp:
            return "smtp.user"
        if "password" not in smtp:
            return "smtp.password"
    else:
        return "smtp"

    if "sender_email" not in config:
        return "sender_email"
    if "recipient_email" not in config:
        return "recipient_email"

    if "zoom" in config:
        zoom = config["zoom"]
        if "link" not in zoom:
            return "zoom.link"
        if "id" not in zoom:
            return "zoom.id"
        if "password" not in zoom:
            return "zoom.password"
    else:
        return "zoom"

    if "room" not in config:
        return "room"

    if "admin" in config:
        admin = config["admin"]
        if "name" not in admin:
            return "admin.name"
        if "email" not in admin:
            return "admin.email"
    else:
        return "admin"

    if "discord" not in config:
        return "discord"

    return ""


def load_config(config_file, log_file):
    with open(config_file) as config_stream:
        config = yaml.safe_load(config_stream)
    check = check_config(config)
    if not check == "":
        debug(log_file, f"Incomplete config, missing field {check}")
        exit(1)
    return Config(config, log_file)

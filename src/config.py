import json
from debug import debug
from scraper import get_talks_page
import calendar

# Modes
ANNOUNCE = 0
REMINDER = 1
ABSTRACT = 2


class ZoomDetails:
    def __init__(self, json):
        self.link = json["link"]
        self.id = json["id"]
        self.password = json["password"]


class AdminDetails:
    def __init__(self, json):
        self.name = json["name"]
        self.email = json["email"]


class SMTPDetails:
    def __init__(self, json):
        self.host = json["host"]
        self.port = json["port"]
        self.user = json["user"]
        self.password = json["password"]


class Daytime:
    def __init__(self, day, time, offset=0):
        self.day = day
        self.time = time
        self.offset = offset


def get_offset_day(day, offset):
    day = day - offset
    if day < 0:
        day = day + 5
    return day


def get_daytime_from_offset(json, default_offset, default_time, origin):
    if json is None:
        offset = default_offset
        time = default_time
    else:
        if "offset" in json:
            offset = json["offset"]
        else:
            offset = default_offset
        if "time" in json:
            time = json["time"]
        else:
            time = default_time
    day = get_offset_day(origin, offset)
    return Daytime(day, time, offset)


def get_daytime(json, default_day, default_time):
    if json is None:
        day = default_day
        time = default_time
    else:
        if "day" in json:
            day = json["day"]
        else:
            day = default_day
        if "time" in json:
            time = json["time"]
        else:
            time = default_time
    return Daytime(day, time)


default_announce_day = 0
default_announce_time = "10:00"
default_reminder_offset = 0
default_reminder_time = "10:00"
default_abstract_offset = 1
default_abstract_time = "10:00"


class Config:
    def __init__(self, json, log_file):
        self.id = json["talks_id"]
        self.page = get_talks_page(self.id)
        self.smtp = SMTPDetails(json["smtp"])
        self.sender_email = json["sender_email"]
        self.recipient_email = json["recipient_email"]
        self.zoom = ZoomDetails(json["zoom"])
        self.room = json["room"]
        self.admin = AdminDetails(json["admin"])
        self.talk_day = json["talk_day"]
        self.talk_day_name = calendar.day_name[self.talk_day]

        self.announce = get_daytime(
            json.get("announce"), default_announce_day, default_announce_time)
        self.reminder = get_daytime_from_offset(
            json.get("reminder"), default_reminder_offset, default_reminder_time, self.talk_day)
        self.abstract = get_daytime_from_offset(json.get(
            "abstract"), default_abstract_offset, default_abstract_time, self.announce.day)

        if "emails" in json:
            self.emails = json["emails"]

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

    return ""


def load_config(config_file, log_file):
    with open(config_file) as config_stream:
        config = json.load(config_stream)
    check = check_config(config)
    if not check == "":
        debug(log_file, f"Incomplete config, missing field {check}")
        exit(1)
    return Config(config, log_file)

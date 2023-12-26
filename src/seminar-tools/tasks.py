import datetime

from debug import debug
from config import ANNOUNCE, REMINDER
from emails import prepare_email, write_and_send_email, write_email
from bot import post_to_discord
from scraper import get_next_talk


def get_template(config, mode):
    if mode == ANNOUNCE:
        return "announce.txt"
    if mode == REMINDER:
        return "reminder.txt"
    debug(config, "Bad mode found while finding template")
    exit(1)


def announce_seminar(config, seminar, talk, stdout):
    template = get_template(config, ANNOUNCE)
    email = write_email(config, seminar, talk, template)
    prepare_email(config, seminar, talk, email)


def reminder_seminar(config, seminar, talk, stdout):
    template = get_template(config, REMINDER)
    write_and_send_email(config, seminar, talk, template, False, stdout)
    if not stdout:
        post_to_discord(config, seminar, talk, REMINDER)


def check_if_right_time(target_datetime):
    today = datetime.datetime.today()
    date = target_datetime.date()
    time = target_datetime.time()
    # We can't be too precise with the time as it might take a few seconds to load the script
    # If running as a cron job, this should be run at most once an hour so you don't get dupes
    return today.date() == date and today.hour == time.hour


def check_for_tasks(config):
    for seminar in config.seminars:
        next_talk = get_next_talk(config, seminar)
        if next_talk is not None:
            if check_if_right_time(next_talk.announce_datetime):
                announce_seminar(config, seminar, next_talk, False)
            elif check_if_right_time(next_talk.reminder_datetime):
                reminder_seminar(config, seminar, next_talk, False)
            else:
                debug(config, f"{seminar.name}: Not the right time to send an email")
        else:
            debug(config, f"No talk in the next week for {seminar.name}")

import json
from scraper import get_next_talk
from emails import write_email, send_email

with open("config.json") as config_file:
    config = json.load(config_file)

next_talk = get_next_talk(config)
email = write_email(config, next_talk)
send_email(config, next_talk, email)

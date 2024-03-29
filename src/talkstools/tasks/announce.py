import sys
from jinja2 import Environment, PackageLoader, select_autoescape

from talkstools.core.structs import (
    Talk,
    get_abstract_string,
    get_speaker_and_affiliation_string,
    get_speaker_string,
    get_title_string,
    get_venue_string,
)
from talkstools.discord.bot import post_to_discord
from talkstools.researchseminars.lookup import (
    get_next_talk_from_series,
    get_researchseminars_url,
)
from talkstools.talks.talk_read import get_abstract, get_talk_index_route
from talkstools.talks.url import get_talks_url


def write_template(name: str, vars: dict) -> str:
    env = Environment(
        loader=PackageLoader("talkstools.tasks"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name)
    text = template.render(vars)
    return text


def write_announcement_email(admin: str, talk: Talk) -> str:
    if talk.series is None:
        series = "seminar"
    else:
        series = talk.series.name
    email = write_template(
        "announce.txt",
        {
            "series": series,
            "speaker_name": get_speaker_string(talk),
            "abstract": get_abstract_string(talk),
            "title": get_title_string(talk),
            "speaker_text": get_speaker_and_affiliation_string(talk),
            "talk_date": talk.talk_start.strftime("%A %d %B %Y"),
            "talk_start": talk.talk_start.strftime("%H:%M"),
            "talk_end": talk.talk_end.strftime("%H:%M"),
            "venue": get_venue_string(talk),
            "admin": admin,
            "url": get_researchseminars_url(talk),
        },
    )
    return email


def write_announcent_discord_message(talk: Talk) -> str:
    if talk.series is None:
        series = "seminar"
    else:
        series = talk.series.name
    if talk.talk_id is None:
        raise RuntimeError("No talk id")
    message = write_template(
        "discord-announce.txt",
        {
            "series": series,
            "speaker_name": get_speaker_string(talk),
            "title": talk.title,
            "talk_date": talk.talk_start.strftime("%A %d %B %Y"),
            "talk_start": talk.talk_start.strftime("%H:%M"),
            "talk_end": talk.talk_end.strftime("%H:%M"),
            "venue": get_venue_string(talk),
            "speaker_text": get_speaker_and_affiliation_string(talk),
            "url": get_researchseminars_url(talk),
        },
    )
    return message


def print_email(email: str):
    print(
        "================================================================================"
    )
    print()
    print(email)
    print()
    print(
        "================================================================================"
    )


def start(admin: str, talk_series: str):
    talk = get_next_talk_from_series(talk_series)
    email = write_announcement_email(admin, talk)
    print_email(email)
    discord_message = write_announcent_discord_message(talk)
    post_to_discord("seminars", discord_message)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <admin name> <series id>")
        exit(1)
    start(sys.argv[1], sys.argv[2])

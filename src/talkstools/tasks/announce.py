from jinja2 import Environment, PackageLoader, select_autoescape

from talkstools.core.structs import (
    Talk,
    get_speaker_and_affiliation_string,
    get_venue_string,
)
from talkstools.talks.talk_read import get_talk_index_route
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
    (speaker_name, speaker_text) = get_speaker_and_affiliation_string(talk)
    if talk.series is None:
        series = "seminar"
    else:
        series = talk.series.name
    email = write_template(
        "announce.txt",
        {
            "series": series,
            "speaker_name": speaker_name,
            "abstract": talk.abstract,
            "title": talk.title,
            "speaker_text": speaker_text,
            "talk_date": talk.talk_date.strftime("%A %d %B %Y"),
            "talk_start": talk.talk_start.strftime("%H:%M"),
            "talk_end": talk.talk_end.strftime("%H:%M"),
            "admin": admin,
        },
    )
    return email


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
from jinja2 import Environment, PackageLoader, select_autoescape

from talkstools.talks.start import start
from talkstools.talks.login import login
from talkstools.talks.pull import get_talk
from talkstools.talks.structs import Talk


def write_email(name: str, vars: dict) -> str:
    env = Environment(
        loader=PackageLoader("talkstools.talks"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name)
    email = template.render(vars)
    return email


def write_announcement_email(admin: str, talk: Talk) -> str:
    if talk.speaker is None:
        speaker_name = "Speaker to be confirmed"
        speaker_text = speaker_name
    else:
        speaker_name = talk.speaker.name
        if talk.speaker.affiliation is None:
            speaker_text = speaker_name
        else:
            speaker_text = f"{speaker_name} ({talk.speaker.affiliation})"
    if talk.series is None:
        series = "seminar"
    else:
        series = talk.series.name
    email = write_email(
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


if __name__ == "__main__":
    driver = start()
    cookie = login(driver)
    talk = get_talk(5615, cookie)
    print(write_announcement_email("George", talk))

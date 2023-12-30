import argparse
import requests
from datetime import date, time, timedelta, datetime


from talkstools.talks.login import (
    get_talks_session_cookies,
    login,
)
from talkstools.core.structs import (
    Talk,
    get_speaker_input_string,
)
from talkstools.talks.start import get_talks_url

edit_talk_route = "talk/edit"


def get_multipart_part(name: str, value: str) -> str:
    return f'Content-Disposition: form-data; name="{name}"\n\n{value}'


def get_talk_multipart_part(key: str, value: str) -> str:
    return get_multipart_part(f"talk[{key}]", value)


def get_talks_title_value(talk: Talk) -> str:
    if talk.title is not None:
        talk_title = talk.title
    else:
        talk_title = "Title to be confirmed"
    return talk_title


def get_talks_abstract_value(talk: Talk) -> str:
    if talk.abstract is not None:
        talk_abstract = talk.abstract
    else:
        talk_abstract = "Abstract to be confirmed"
    return talk_abstract


def get_talks_speaker_values(talk: Talk) -> tuple[str, str]:
    if talk.speaker is not None:
        if talk.speaker.email is not None:
            speaker_email = talk.speaker.email
        else:
            speaker_email = ""
        if talk.speaker.name is not None:
            speaker_name = get_speaker_input_string(talk)
        else:
            speaker_name = "Speaker to be confirmed"
    else:
        speaker_name = "Speaker to be confirmed"
        speaker_email = ""
    return (speaker_email, speaker_name)


def get_talks_organiser_value(talk: Talk) -> str:
    if talk.organiser is not None and talk.organiser.email is not None:
        organiser_email = talk.organiser.email
    else:
        organiser_email = ""
    return organiser_email


def get_talks_special_value(talk: Talk) -> str:
    if talk.special_message is not None:
        special_message = talk.special_message
    else:
        special_message = ""
    return special_message


def get_talks_venue_value(talk: Talk) -> str:
    if talk.venue is not None:
        venue = talk.venue
    else:
        venue = "Venue to be confirmed"
    return venue


def get_update_parts(talk: Talk) -> dict[str, str]:
    parts = {}
    parts["talk[series_id]"] = str(talk.series_id)
    parts["talk[title]"] = get_talks_title_value(talk)
    parts["talk[abstract]"] = get_talks_abstract_value(talk)
    (speaker_email_value, speaker_name_value) = get_talks_speaker_values(talk)
    parts["talk[speaker_email]"] = speaker_email_value
    parts["talk[name_of_speaker]"] = speaker_name_value
    parts["talk[send_speaker_email]"] = "0"
    parts["talk[organiser_email]"] = get_talks_organiser_value(talk)
    parts["talk[special_message]"] = get_talks_special_value(talk)
    parts["talk[venue_name]"] = get_talks_venue_value(talk)
    parts["talk[date_string]"] = talk.talk_date.strftime("%Y/%m/%d")
    parts["talk[start_time_string]"] = talk.talk_start.strftime("%H:%M")
    parts["talk[end_time_string]"] = talk.talk_end.strftime("%H:%M")
    parts["commit"] = "Save"
    return parts


def update_talk(talk_id: int, talk: Talk, session_id: str):
    parts = get_update_parts(talk)
    url = get_talks_url(f"talk/update/{talk_id}")
    requests.post(url, files=parts, cookies=get_talks_session_cookies(session_id))


def add_talk(talk: Talk, session_id: str):
    parts = get_update_parts(talk)
    url = get_talks_url("talk/update")
    requests.post(url, files=parts, cookies=get_talks_session_cookies(session_id))


def add_talks_in_range(
    list_id: int,
    start_date: date,
    end_date: date,
    day: int,
    start_time: time,
    end_time: time,
    session_id: str,
):
    start_day = start_date.weekday()
    current_date = start_date + timedelta(days=abs(day - start_day))
    while current_date <= end_date:
        talk = Talk(list_id, current_date, start_time, end_time)
        add_talk(talk, session_id)
        current_date = current_date + timedelta(days=7)


parser = argparse.ArgumentParser(prog="populate", description="Add talks")

parser.add_argument("-l", "--list")

parser.add_argument("-t", "--time", nargs=2)

parser.add_argument("-d", "--date")

parser.add_argument("-r", "--range", nargs=2, metavar="DATE")
parser.add_argument("-w", "--day")


def main():
    args = parser.parse_args()

    if (
        ((args.date is None) and (args.range is None or args.day is None))
        or args.list is None
        or args.time is None
    ):
        parser.print_usage()
    else:
        talk_list = int(args.list)
        start_time = datetime.strptime(args.time[0], "%H:%M").time()
        end_time = datetime.strptime(args.time[1], "%H:%M").time()
        session_id = login()
        if not (args.date is None or args.time is None):
            talk_date = datetime.strptime(args.date, "%Y-%m-%d").date()
            talk = Talk(talk_list, talk_date, start_time, end_time)
            add_talk(talk, session_id)
        elif not (args.range is None or args.day is None):
            start_date = datetime.strptime(args.range[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(args.range[1], "%Y-%m-%d").date()
            day = int(args.day)
            add_talks_in_range(
                talk_list,
                start_date,
                end_date,
                day,
                start_time,
                end_time,
                session_id,
            )


if __name__ == "__main__":
    main()

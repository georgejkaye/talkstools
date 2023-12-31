import argparse
import requests

from datetime import datetime, date, time, timedelta

from talkstools.core.structs import (
    Talk,
    get_speaker_and_affiliation_string,
    get_talk_string,
)
from talkstools.talks.login import get_talks_session_cookies, login
from talkstools.talks.url import get_talks_url


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
        (_, speaker_name) = get_speaker_and_affiliation_string(talk)
        if talk.speaker.email is not None:
            speaker_email = talk.speaker.email
        else:
            speaker_email = ""
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


def get_update_talk_route(talk_id: int) -> str:
    return f"talk/update/{talk_id}"


def update_talk(talk_id: int, talk: Talk, session_id: str):
    print(f"Updating talk {get_talk_string(talk)}")
    parts = get_update_parts(talk)
    url = get_talks_url(get_update_talk_route(talk_id))
    response = requests.post(
        url, files=parts, cookies=get_talks_session_cookies(session_id)
    )
    if response.status_code == 401:
        raise SystemExit(f"Not authorised to update talk {talk_id}")
    if response.status_code != 200:
        raise SystemExit(f"Error {response.status_code}: could not update talk.")


def get_add_talk_route() -> str:
    return "talk/update"


def add_talk(talk: Talk, session_id: str):
    print(f"Adding talk {get_talk_string(talk)} to list {talk.series_id}")
    parts = get_update_parts(talk)
    url = get_talks_url(get_add_talk_route())
    response = requests.post(
        url, files=parts, cookies=get_talks_session_cookies(session_id)
    )
    if response.status_code == 401:
        raise SystemExit(
            f"Not authorised to add talk {talk.id} to list {talk.series_id}"
        )
    if response.status_code != 200:
        raise SystemExit(f"Error {response.status_code}: could not remove talk.")


def get_remove_talk_route(talk_id: int) -> str:
    return f"talk/delete/{talk_id}"


def remove_talk(talk_id: int, session_id: str):
    print(f"Removing talk {talk_id}")
    url = get_talks_url(get_remove_talk_route(talk_id))
    data = {"commit": "Delete+Talk"}
    response = requests.post(
        url,
        data=data,
        cookies=get_talks_session_cookies(session_id),
    )
    if response.status_code == 401:
        raise SystemExit(f"Not authorised to remove talk {talk_id}")
    if response.status_code != 200:
        raise SystemExit(f"Error {response.status_code}: could not remove talk.")


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

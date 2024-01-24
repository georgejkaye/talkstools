from datetime import datetime, timezone
from typing import Optional
import requests

from talkstools.core.structs import Person, Talk


def get_talk_url(talk_series: str, talk_id: int) -> str:
    return f'https://researchseminars.org/api/0/lookup/talk?series_id="{talk_series}"&series_ctr={talk_id}'


def get_series_url(talk_series: str) -> str:
    return f'https://researchseminars.org/api/0/lookup/series?series_id="{talk_series}"'


def get_researchseminars_url(talk: Talk) -> str:
    return f"https://researchseminars.org/talk/{talk.series_id}/{talk.talk_id}/"


def get_property_or_none(properties: dict, field: str) -> Optional[str]:
    value = properties[field]
    if value == "":
        return None
    return value


def get_talk_from_json(properties: dict) -> Talk:
    seminar_id = properties["seminar_id"]
    start_datetime = datetime.fromisoformat(properties["start_time"]).astimezone(
        timezone.utc
    )
    end_datetime = datetime.fromisoformat(properties["end_time"]).astimezone(
        timezone.utc
    )
    talk_title = get_property_or_none(properties, "title")
    talk_abstract = get_property_or_none(properties, "abstract")
    speaker_name = get_property_or_none(properties, "speaker")
    speaker_email = get_property_or_none(properties, "speaker_email")
    speaker_affil = get_property_or_none(properties, "speaker_affiliation")
    speaker_web = get_property_or_none(properties, "speaker_homepage")
    if speaker_name is None:
        speaker = None
    else:
        speaker = Person(speaker_name, speaker_email, speaker_affil, speaker_web)
    talk_id = properties["seminar_ctr"]
    seminar_id = properties["seminar_id"]
    venue = properties["room"]
    return Talk(
        seminar_id,
        start_datetime,
        end_datetime,
        talk_title,
        talk_abstract,
        speaker,
        talk_id,
        venue,
    )


def get_talk(talk_series: str, talk_id: int) -> Talk:
    url = get_talk_url(talk_series, talk_id)
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        properties = json["properties"]
        return get_talk_from_json(properties)
    else:
        raise RuntimeError("Could not get talk")


def get_talks_from_series(talk_series: str) -> list[Talk]:
    url = get_series_url(talk_series)
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        talks = json["talks"]
        talks_list = [get_talk_from_json(properties) for properties in talks]
        return talks_list
    else:
        raise RuntimeError("Could not get series")


def get_next_talk_from_series(talk_series: str) -> Talk:
    talks = get_talks_from_series(talk_series)
    if len(talks) == 0:
        exit(0)
    talk = talks[0]
    return talk

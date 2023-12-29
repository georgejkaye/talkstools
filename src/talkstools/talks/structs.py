from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Series:
    name: str
    id: Optional[int] = None


@dataclass
class Talk:
    talk_date: date
    talk_start: time
    talk_end: time
    title: Optional[str] = None
    abstract: Optional[str] = None
    speaker_email: Optional[str] = None
    speaker_name_and_affiliation: Optional[str] = None
    organiser_name: Optional[str] = None
    organiser_email: Optional[str] = None
    special_message: Optional[str] = None
    id: Optional[int] = None
    venue: Optional[str] = None
    series: Optional[Series] = None


def get_title_string(talk: Talk) -> str:
    if talk.title is None:
        return "Title to be confirmed"
    return talk.title


def get_speaker_string(talk: Talk) -> str:
    if talk.speaker_name_and_affiliation is None:
        return "Speaker to be confirmed"
    return talk.speaker_name_and_affiliation


def get_datetime_string(talk: Talk) -> str:
    return f"{talk.talk_date.strftime('%d %b %Y')} {talk.talk_start.strftime('%H:%M')}-{talk.talk_end.strftime('%H:%M')}"


def get_talk_string(talk: Talk) -> str:
    return f"'{get_title_string(talk)}' - {get_speaker_string(talk)} ({get_datetime_string(talk)})"

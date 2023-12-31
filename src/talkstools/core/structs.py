from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional


@dataclass
class Series:
    id: int
    name: str


@dataclass
class User:
    name: str
    email: Optional[str] = None
    affiliation: Optional[str] = None


@dataclass
class ShortTalk:
    series_id: int
    talk_id: int
    title: str
    abstract: str
    speaker: str
    venue: str
    special_message: str
    url: str
    start_time: datetime
    end_time: datetime


def get_short_talk_datetime_string(talk: ShortTalk) -> str:
    return f"{talk.start_time.strftime('%d %b %Y')} {talk.start_time.strftime('%H:%M')}-{talk.end_time.strftime('%H:%M')}"


def get_short_talk_string(talk: ShortTalk) -> str:
    return f"{talk.talk_id}: '{talk.title}' - {talk.speaker} ({get_short_talk_datetime_string(talk)})"


def get_short_talk_table(talks: list[ShortTalk]) -> str:
    max_id_length = max([len(str(talk.talk_id)) for talk in talks])
    max_title_length = max([len(talk.title) for talk in talks])
    max_speaker_length = max([len(talk.speaker) for talk in talks])
    strings = []
    for talk in talks:
        id_string = str(talk.talk_id).ljust(max_id_length)
        title_string = talk.title.ljust(max_title_length)
        speaker_string = talk.speaker.ljust(max_speaker_length)
        datetime_string = get_short_talk_datetime_string(talk)
        talk_string = (
            f"{id_string}   {title_string}   {speaker_string}   {datetime_string}"
        )
        strings.append(talk_string)
    return "\n".join(strings)


@dataclass
class Talk:
    series_id: int
    talk_date: date
    talk_start: time
    talk_end: time
    series_name: Optional[str] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    speaker: Optional[User] = None
    organiser: Optional[User] = None
    special_message: Optional[str] = None
    id: Optional[int] = None
    venue: Optional[str] = None
    series: Optional[Series] = None


def get_title_string(talk: Talk) -> str:
    if talk.title is None:
        return "Title to be confirmed"
    return talk.title


def get_speaker_input_string(talk: Talk) -> str:
    if talk.speaker is None:
        return ""
    if talk.speaker.affiliation is None:
        return talk.speaker.name
    return f"{talk.speaker.name} ({talk.speaker.affiliation})"


def get_speaker_string(talk: Talk) -> str:
    if talk.speaker is None:
        return "Speaker to be confirmed"
    return talk.speaker.name


def get_datetime_string(talk: Talk) -> str:
    return f"{talk.talk_date.strftime('%d %b %Y')} {talk.talk_start.strftime('%H:%M')}-{talk.talk_end.strftime('%H:%M')}"


def get_talk_string(talk: Talk) -> str:
    return f"'{get_title_string(talk)}' - {get_speaker_string(talk)} ({get_datetime_string(talk)})"

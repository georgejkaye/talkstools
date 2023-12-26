from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Talk:
    talk_date: date
    talk_start: time
    talk_end: time
    title: Optional[str] = None
    abstract: Optional[str] = None
    speaker_email: Optional[str] = None
    speaker_name_and_affiliation: Optional[str] = None
    organiser_email: Optional[str] = None
    special_message: Optional[str] = None
    venue: Optional[str] = None
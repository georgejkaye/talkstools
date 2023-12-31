from datetime import datetime
from typing import Optional
from lxml import etree
from lxml.etree import _Element as Element
from talkstools.core.structs import ShortTalk

from talkstools.talks.talk_read import requests_get
from talkstools.talks.url import get_talks_url

series_xml_route = "show/xml"


def get_series_xml_url(series_id: int, days: Optional[int] = None) -> str:
    options = []
    if days:
        seconds = days * 86400
        options.append(("seconds_before_today", 0))
        options.append(("seconds_after_today", seconds))
    route = f"{series_xml_route}/{series_id}"
    return get_talks_url(route, options)


def get_series_xml(series_id: int, days: Optional[int] = None) -> Element:
    url = get_series_xml_url(series_id, days)
    data = requests_get(url)
    root = etree.fromstring(data)
    return root


def find_or_fail(element: Element, tag: str) -> str:
    tag_elem = element.find(tag)
    if tag_elem is None:
        raise RuntimeError(f"Could not find {tag} in {element}")
    if tag_elem.text is None:
        return ""
    return tag_elem.text


def get_short_talks_from_series_xml(root: Element) -> list[ShortTalk]:
    series_id = int(find_or_fail(root, "id"))
    talks = root.findall("talk")
    talk_objects = []
    for talk in talks:
        talk_id = int(find_or_fail(talk, "id"))
        title = find_or_fail(talk, "title")
        abstract = find_or_fail(talk, "abstract")
        speaker = find_or_fail(talk, "speaker")
        venue = find_or_fail(talk, "venue")
        special = find_or_fail(talk, "special_message")
        url = find_or_fail(talk, "url")
        datetime_format = "%a, %d %b %Y %H:%M:%S %z"
        start_time = datetime.strptime(
            find_or_fail(talk, "start_time"), datetime_format
        )
        end_time = datetime.strptime(find_or_fail(talk, "end_time"), datetime_format)
        talk_object = ShortTalk(
            series_id,
            talk_id,
            title,
            abstract,
            speaker,
            venue,
            special,
            url,
            start_time,
            end_time,
        )
        talk_objects.append(talk_object)
    return talk_objects


def get_talk_with_series(talk_id: int, series_id: int) -> Element:
    xml = get_series_xml(series_id)
    talks = xml.findall("talk")
    for talk in talks:
        id = talk.find("id")
        if id is not None and id.text is not None and int(id.text) == talk_id:
            return talk
    raise SystemExit(f"Talk {talk_id} not found in series {series_id}")

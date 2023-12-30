from typing import Optional
from lxml import etree
from lxml.etree import _Element as Element

from talkstools.talks.pull import requests_get
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


def get_talk_with_series(talk_id: int, series_id: int) -> Element:
    xml = get_series_xml(series_id)
    talks = xml.findall("talk")
    for talk in talks:
        id = talk.find("id")
        if id is not None and id.text is not None and int(id.text) == talk_id:
            return talk
    raise SystemExit(f"Talk {talk_id} not found in series {series_id}")

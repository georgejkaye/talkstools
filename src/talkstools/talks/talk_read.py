import requests

from datetime import datetime
from typing import Optional
from lxml import etree
from lxml.etree import _Element as Element

from talkstools.core.structs import Series, Talk, Person
from talkstools.talks.url import get_talks_url

talk_index_route = "talk/index"


def requests_get(url: str, cookies: dict = {}) -> bytes:
    page = requests.get(url, cookies=cookies)
    if page.status_code != 200:
        raise SystemExit(f"Could not get page {url}")
    return page.content


def get_breadcrumbs(root: Element) -> Element:
    breadcrumbs = root.xpath(".//div[@id = 'bread']")[0]
    if breadcrumbs is None:
        raise SystemExit("Could not find breadcrumb trail")
    return breadcrumbs


def get_series_from_breadcrumbs(breadcrumbs: Element) -> Series:
    series = breadcrumbs.xpath("(.//a)[3]")[0]
    if series is None or series.text is None:
        raise SystemExit("Could not find series item in breadcrumb trail")
    series_name = series.text
    if series_name is None:
        raise SystemExit("Could not find series name")
    series_url = series.get("href")
    if series_url is None:
        raise SystemExit("Could not find series url")
    series_id = int(series_url.split("/")[-1])
    return Series(series_id, series_name)


def get_title(root: Element) -> str:
    header = root.xpath(".//h1[@class= 'summary']")[0]
    if header is None or header.text is None:
        raise SystemExit("Could not find title")
    return header.text


def get_details(root: Element) -> Element:
    details = root.xpath(".//ul[@class = 'details']")[0]
    if details is None:
        raise SystemExit("Could not find details")
    return details


def get_item_from_user(root: Element, elem: int) -> str:
    item = root.xpath("(//div[@class = 'user']//td)[$elem]", elem=elem)[0]
    if item is None or item.text is None:
        raise SystemExit("Could not find speaker")
    return item.text


def get_show_user_route(user_id: int) -> str:
    return f"/user/show/{user_id}"


def get_person(user_id: int, cookie: str) -> Person:
    speaker_url = get_talks_url(get_show_user_route(user_id))
    speaker_page = requests_get(speaker_url, cookies={"_session_id": cookie})
    speaker_root = etree.HTML(speaker_page)
    speaker_name = get_item_from_user(speaker_root, 2)
    speaker_affiliation = get_item_from_user(speaker_root, 4)
    speaker_email_item = speaker_root.xpath(
        "((//div[@class = 'user']//td)[$elem])/a", elem=6
    )[0]
    if speaker_email_item is None or speaker_email_item.text is None:
        raise SystemExit("Could not find speaker email")
    speaker_email = speaker_email_item.text
    return Person(speaker_name, speaker_email, speaker_affiliation)


def get_speaker_from_details(details: Element, cookie: str) -> Optional[Person]:
    speaker_item = details.xpath("(.//li)[1]")[0]
    if speaker_item is None:
        raise SystemExit("Could not find speaker")
    speaker_link = speaker_item.find("a")
    if speaker_link is None:
        text = "".join(speaker_item.itertext())
        if text == "Speaker to be confirmed":
            return None
        return Person(text)
    speaker_route = speaker_link.get("href")
    speaker_id = int(speaker_route.split("/")[-1])
    return get_person(speaker_id, cookie)


def get_times_from_details(details: Element) -> tuple[datetime, datetime]:
    time_detail = details.xpath("(.//li)[2]")[0]
    if time_detail is None:
        raise SystemExit("Could not get time")
    time_text = "".join(time_detail.itertext())
    date_and_times = time_text.split(",")
    date_text = date_and_times[0]
    date_object = datetime.strptime(date_text, "%A %d %B %Y").date()
    times = date_and_times[1][1:].split("-")
    start_text = times[0]
    start_object = datetime.strptime(start_text, "%H:%M").time()
    end_text = times[1]
    end_object = datetime.strptime(end_text, "%H:%M").time()
    return (
        datetime.combine(date_object, start_object),
        datetime.combine(date_object, end_object),
    )


def get_venue_from_details(details: Element) -> Optional[str]:
    venue_detail = details.xpath("(.//li)[3]")[0]
    if venue_detail is None:
        raise SystemExit("Could not find venue")
    venue_item = venue_detail.find("a")
    if venue_item is None or venue_item.text is None:
        raise SystemExit("Could not find venue")
    if venue_item.text == "Venue to be confirmed":
        return None
    return venue_item.text


def get_special(root: Element) -> Optional[str]:
    special = root.xpath(".//p[@class = 'urgent']")[0]
    if special is None or special.text is None:
        return None
    return special.text


def get_organiser(root: Element, cookie) -> Person:
    organiser = root.xpath("((.//div[@class = 'vevent']/p)[2])/a")[0]
    if organiser is None or organiser.text is None:
        raise SystemExit("Could not find organiser")
    organiser_route = organiser.get("href")
    if organiser_route is None:
        raise SystemExit("could not find organiser")
    organiser_id = int(organiser_route.split("/")[-1])
    return get_person(organiser_id, cookie)


def get_abstract(root: Element) -> str:
    ps = root.xpath("//div[@class='vevent']/p")
    abstract_paragraphs = []
    in_abstract = False
    for p in ps:
        if not in_abstract and p.get("class") == "urgent":
            in_abstract = True
        elif in_abstract:
            if p.text is not None:
                if "This talk is part of the" in p.text:
                    in_abstract = False
                    break
                else:
                    abstract_paragraphs.append(p.text)
    if len(abstract_paragraphs) == 0:
        return "Abstract not available"
    return "\n".join(abstract_paragraphs)


def get_talk_index_route(talk_id: int) -> str:
    return f"talk/index/{talk_id}"


def get_talk(talk_id: int, session_id: str):
    url = get_talks_url(get_talk_index_route(talk_id))
    page = requests_get(url, cookies={"_session_id": session_id})
    root = etree.HTML(page)
    breadcrumbs = get_breadcrumbs(root)
    talk_series = get_series_from_breadcrumbs(breadcrumbs)
    talk_title = get_title(root)
    talk_details = get_details(root)
    talk_speaker = get_speaker_from_details(talk_details, session_id)
    (talk_start, talk_end) = get_times_from_details(talk_details)
    talk_venue = get_venue_from_details(talk_details)
    talk_abstract = get_abstract(root)
    return Talk(
        talk_series.id,
        talk_start,
        talk_end,
        talk_title,
        talk_abstract,
        talk_speaker,
        talk_id,
        talk_venue,
    )

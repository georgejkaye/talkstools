import re
import requests
from bs4 import BeautifulSoup

datetime_regex = r'([A-Za-z]+) ([0-3][0-9]) ([A-Za-z]+) ([0-9][0-9][0-9][0-9]), ([0-2][0-9]:[0-5][0-9])-([0-2][0-9]:[0-5][0-9])'
speaker_regex = r'([A-Za-z ]+)( \(.*\))?\.'


class Datetime:
    def __init__(self, string):
        self.string = string
        groups = re.search(datetime_regex, string)
        self.day = groups.group(1)
        self.date = groups.group(2)
        self.month = groups.group(3)
        self.year = groups.group(4)
        self.start_time = groups.group(5)
        self.end_time = groups.group(6)

    def get_short_string(self):
        return f"{self.day} {self.date} {self.month} @ {self.start_time}"


class Talk:
    def __init__(self, title, speaker, link, datetime, abstract):
        self.title = title
        self.speaker = speaker
        self.link = link
        self.datetime = datetime
        self.abstract = abstract


def make_request(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(f"Error {page.status_code}: could not get page {link}")
        exit(1)
    return page.content


def get_next_talk(config):
    bravo_page = config["page"]

    upcoming_talks = make_request(bravo_page)

    soup = BeautifulSoup(upcoming_talks, "html.parser")
    talks = soup.find_all("div", class_="vevent")
    next_talk = talks[0]
    next_talk_children = list(next_talk.children)

    talk_heading = list(next_talk_children[1].children)[0]
    talk_link = talk_heading["href"]
    talk_title = talk_heading.text

    speaker_entry = list(next_talk_children[5].children)[1].text
    talk_speaker = re.search(speaker_regex, speaker_entry).group(1)

    date_entry = list(next_talk_children[9].children)
    talk_datetime = Datetime(date_entry[1].text + "-" + date_entry[3].text)

    talk_page = make_request(talk_link)

    soup = BeautifulSoup(talk_page, "html.parser")
    talk_paragraphs = soup.find("div", class_="vevent").find_all("p")

    # By default, there are five p elements with no abstract
    if len(talk_paragraphs) > 5:
        abstract_paragraphs = talk_paragraphs[3:-2]
        abstract_string = abstract_paragraphs[0].text
        for abs in abstract_paragraphs[1:]:
            abstract_string = abstract_string + "\n\n" + abs.text
    else:
        abstract_string = "Abstract to be confirmed"

    return Talk(talk_title, talk_speaker, talk_link, talk_datetime, abstract_string)

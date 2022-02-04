import re
import requests
import datetime
from bs4 import BeautifulSoup

datetime_regex = r'([A-Za-z]+) ([0-3][0-9]) ([A-Za-z]+) ([0-9][0-9][0-9][0-9]), ([0-2][0-9]:[0-5][0-9])-([0-2][0-9]:[0-5][0-9])'
speaker_regex = r'([A-Za-z ]+)( \(.*\))?\.'


class Talk:
    def __init__(self, title, speaker, link, date, start, end, abstract):
        self.title = title
        self.speaker = speaker
        self.link = link
        self.date = date
        self.start = start
        self.end = end
        self.abstract = abstract

    def get_long_datetime(self):
        return datetime.datetime.strftime(self.date, "%A %d %B %Y") + ", " + self.start + "-" + self.end

    def get_mid_datetime(self):
        return datetime.datetime.strftime(self.date, "%A %d %B")

    def get_short_datetime(self):
        return datetime.datetime.strftime(self.date, "%a %d %b") + " @ " + self.start


talks_url_base = "http://talks.bham.ac.uk/show/index/"


def make_request(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(f"Error {page.status_code}: could not get page {link}")
        exit(1)
    return page.content


def in_next_days(date, range):
    today = datetime.datetime.today()
    range = datetime.timedelta(days=range)
    return date <= today + range


def get_next_talk(config, range):
    bravo_page = talks_url_base + str(config["talks_id"])

    upcoming_talks = make_request(bravo_page)

    soup = BeautifulSoup(upcoming_talks, "html.parser")
    talks = soup.find_all("div", class_="vevent")

    if len(talks) > 0:
        next_talk = talks[0]
        next_talk_children = list(next_talk.children)

        date_entry = list(next_talk_children[9].children)
        talk_datetime_string = date_entry[1].text
        date_string = talk_datetime_string[0:-7]
        talk_date = datetime.datetime.strptime(
            date_string, "%A %d %B %Y")
        talk_start = talk_datetime_string[-5:]
        talk_end = date_entry[3].text

        if not in_next_days(talk_date, range):
            print("Next talk not in range")
            return None

        talk_heading = list(next_talk_children[1].children)[0]
        talk_link = talk_heading["href"]
        talk_title = talk_heading.text

        speaker_entry = list(next_talk_children[5].children)[1].text
        talk_speaker = re.search(speaker_regex, speaker_entry).group(1)

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

        return Talk(talk_title, talk_speaker, talk_link, talk_date, talk_start, talk_end, abstract_string)
    return None

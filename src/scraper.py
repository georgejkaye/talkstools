import re
import requests
import datetime
import xml.etree.ElementTree as ET
from textwrap import fill
from html import unescape
from debug import debug

datetime_regex = r'([A-Za-z]+) ([0-3][0-9]) ([A-Za-z]+) ([0-9][0-9][0-9][0-9]), ([0-2][0-9]:[0-5][0-9])-([0-2][0-9]:[0-5][0-9])'
speaker_regex = r'([A-Za-z ]+) (\((.*)\))?'
speaker_url_regex = r'\"\/user\/show\/([0-9]*)\"'

line_width = 80


def wrap_string(string, width):
    """
    Wrap a string at a given line width.

    Nabbed from https://stackoverflow.com/a/26538082
    """
    paragraphs = string.split("\n")
    output = fill(paragraphs[0], width)
    for para in paragraphs[1:]:
        output = output + "\n" + fill(para, width)
    return output


class Talk:
    def __init__(self, title, speaker, speaker_email, institution, link, date, start, end, abstract):
        self.title = title
        self.speaker = speaker
        self.email = speaker_email
        self.institution = institution
        self.link = link
        self.date = date
        self.start = start
        self.end = end
        self.abstract = wrap_string(abstract, line_width)
        self.has_missing_components = self.title == "Title to be confirmed" or self.abstract == "Abstract not available"

    def get_long_datetime(self):
        return datetime.datetime.strftime(self.date, "%A %d %B %Y") + ", " + self.start + "-" + self.end

    def get_mid_datetime(self):
        return datetime.datetime.strftime(self.date, "%A %d %B")

    def get_short_datetime(self):
        return datetime.datetime.strftime(self.date, "%a %d %b") + " @ " + self.start


talks_url_base = "http://talks.bham.ac.uk"


def get_talks_page(id):
    return f"{talks_url_base}/show/index/{id}"


def get_speaker_page(id):
    return f"{talks_url_base}/user/show/{id}"


def get_talks_xml_url(id, range):
    seconds_in_day = 86400
    seconds = range * seconds_in_day
    return f"{talks_url_base}/show/xml/{id}?seconds_before_today=0&seconds_after_today={seconds}"


def make_request(config, link):
    page = requests.get(link)
    if page.status_code != 200:
        debug(config.log,
              f"Error {page.status_code}: could not get page {link}")
        exit(1)
    return page.content


def in_next_days(date, range):
    today = datetime.datetime.today()
    range = datetime.timedelta(days=range)
    return date <= today + range


def get_next_talk(config, range):
    """
        Get the next talk in a given range (of days). Returns None if there is no such talk.
    """
    bravo_page = get_talks_xml_url(config.id, range)

    upcoming_talks = make_request(config, bravo_page)

    tree = ET.ElementTree(ET.fromstring(upcoming_talks))
    root = tree.getroot()

    talk = root.find("talk")

    if talk is not None:
        talk_title = unescape(talk.find("title").text)
        talk_speaker_and_institution = talk.find("speaker").text
        speaker_matches = re.search(
            speaker_regex, talk_speaker_and_institution)
        talk_speaker = speaker_matches.group(1)
        # Unfortunately (and probably sensibly) you can't get emails from talks
        # unless you're logged in, and I don't know how to do that from within
        # this python script. Instead, we just keep a list of emails in the config
        # file that we can use.  Make sure these emails are in the public domain to
        # keep in line with GDPR regulations!
        talk_speaker_email = config.emails.get(talk_speaker)
        talk_institution = speaker_matches.group(3)
        talk_link = talk.find("url").text
        talk_start_date_and_time = talk.find("start_time").text
        date_string = talk_start_date_and_time[0:-15]
        talk_date = datetime.datetime.strptime(
            date_string, "%a, %d %b %Y")
        talk_start = talk_start_date_and_time[-14:-9]
        talk_end = talk.find("end_time").text[-14:-9]
        abstract_string = talk.find("abstract").text

        # In a perfect world we would have separate fields for all the zoom stuff.
        # Unfortunately talks was made in the noughties and there were no major global
        # pandemics at that point. As a workaround I try to have an *Abstract* tag to
        # distinguish where the abstract proper starts. If this is found, then all the
        # text after this will be put in. Otherwise, the whole textbox will be dumped in.
        split_at_abstract_tag = abstract_string.split("*Abstract*\n\n")

        if len(split_at_abstract_tag) > 1:
            abstract_string = split_at_abstract_tag[-1]
        else:
            abstract_string = split_at_abstract_tag[0]

        return Talk(talk_title, talk_speaker, talk_speaker_email, talk_institution, talk_link, talk_date, talk_start, talk_end, abstract_string)
    return None

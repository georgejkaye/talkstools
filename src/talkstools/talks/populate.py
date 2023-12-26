from datetime import date, time, timedelta
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from talkstools.talks.structs import Talk
from talkstools.talks.start import get_talks_url
from talkstools.talks.utils import fill_box, fill_box_if_not_none

edit_talk_route = "talk/edit"


def add_talk(driver: WebDriver, list_id: int, talk: Talk):
    url = get_talks_url(edit_talk_route, [("list_id", str(list_id))])
    driver.get(url)
    fill_box_if_not_none(driver, By.ID, "talk_title", talk.title)
    fill_box_if_not_none(driver, By.ID, "talk_abstract", talk.abstract)
    fill_box_if_not_none(
        driver, By.ID, "talk_name_of_speaker", talk.speaker_name_and_affiliation
    )
    fill_box_if_not_none(driver, By.ID, "talk_organiser_email", talk.organiser_email)
    fill_box_if_not_none(driver, By.ID, "talk_special_message", talk.special_message)
    fill_box_if_not_none(driver, By.ID, "talk_venue_name", talk.venue)
    fill_box(driver, By.ID, "talk_date_string", talk.talk_date.strftime("%Y/%m/%d"))
    fill_box(driver, By.ID, "talk_start_time_string", talk.talk_start.strftime("%H:%M"))
    box = fill_box(
        driver, By.ID, "talk_end_time_string", talk.talk_end.strftime("%H:%M")
    )
    box.submit()


def add_talks_in_range(
    driver: WebDriver,
    list_id: int,
    start_date: date,
    end_date: date,
    day: int,
    start_time: time,
    end_time: time,
):
    start_day = start_date.weekday()
    current_date = start_date + timedelta(days=abs(day - start_day))
    while current_date <= end_date:
        talk = Talk(current_date, start_time, end_time)
        add_talk(driver, list_id, talk)
        current_date = current_date + timedelta(days=7)

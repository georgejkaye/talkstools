import argparse

from datetime import date, time, timedelta, datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from talkstools.talks.login import TalksCredentials, login
from talkstools.talks.structs import Talk, get_talk_string
from talkstools.talks.start import get_talks_url, start
from talkstools.talks.utils import fill_box, fill_box_if_not_none

edit_talk_route = "talk/edit"


def add_talk(driver: WebDriver, list_id: int, talk: Talk):
    print(f"Adding {get_talk_string(talk)}")
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


parser = argparse.ArgumentParser(prog="populate", description="Add talks")

parser.add_argument("-l", "--list")

parser.add_argument("-t", "--time", nargs=2)

parser.add_argument("-d", "--date")

parser.add_argument("-r", "--range", nargs=2, metavar="DATE")
parser.add_argument("-w", "--day")


def main():
    args = parser.parse_args()

    if (
        ((args.date is None) and (args.range is None or args.day is None))
        or args.list is None
        or args.time is None
    ):
        parser.print_usage()
    else:
        talk_list = args.list
        start_time = datetime.strptime(args.time[0], "%H:%M").time()
        end_time = datetime.strptime(args.time[1], "%H:%M").time()
        driver = start()
        login(driver)

        if not (args.date is None or args.time is None):
            talk = Talk(args.date, start_time, end_time)
            add_talk(driver, talk_list, talk)
        elif not (args.range is None or args.day is None):
            start_date = datetime.strptime(args.range[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(args.range[1], "%Y-%m-%d").date()
            day = int(args.day)
            add_talks_in_range(
                driver, talk_list, start_date, end_date, day, start_time, end_time
            )


if __name__ == "__main__":
    main()

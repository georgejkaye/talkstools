from typing import Sequence

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException

talks_endpoint = "http://talks.bham.ac.uk"


def get_talks_url(route: str, options: Sequence[tuple[str, str]] = []) -> str:
    base_url = f"{talks_endpoint}/{route}"
    if len(options) != 0:
        options_string = "&".join(list(map(lambda x: f"{x[0]}={x[1]}", options)))
        final_url = f"{base_url}?{options_string}"
    else:
        final_url = base_url
    return final_url


def driver_get(driver: WebDriver, url: str):
    try:
        driver.get(url)
    except UnexpectedAlertPresentException:
        driver.switch_to.alert.dismiss()
        driver.get(url)


def start() -> WebDriver:
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver

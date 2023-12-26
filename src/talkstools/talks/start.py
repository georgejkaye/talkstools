from typing import Sequence
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

talks_endpoint = "http://talks.bham.ac.uk"


def get_talks_url(route: str, options: Sequence[tuple[str, str]] = []) -> str:
    options_string = "&".join(list(map(lambda x: f"{x[0]}={x[1]}", options)))
    return f"{talks_endpoint}/{route}?{options_string}"


def start() -> WebDriver:
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver

from dataclasses import dataclass
from typing import Optional
import urllib.parse
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from talkstools.auth import read_credentials
from talkstools.talks.start import get_talks_url
from talkstools.talks.utils import fill_box, wait_and_get

login_route = "login/other_users"
invalid_route = "login/not_raven_login"


@dataclass
class TalksCredentials:
    user: str
    password: str


def get_talks_credentials() -> TalksCredentials:
    credentials_dict = read_credentials()["talks"]
    credentials = TalksCredentials(
        credentials_dict["user"], credentials_dict["password"]
    )
    return credentials


def login_with(
    endpoint: str, driver: WebDriver, credentials: Optional[TalksCredentials] = None
):
    print("Logging in...")
    if credentials is None:
        talks_credentials = get_talks_credentials()
    else:
        talks_credentials = credentials
    driver.get(endpoint)
    fill_box(driver, By.ID, "email", talks_credentials.user)
    password_box = fill_box(driver, By.ID, "password", talks_credentials.password)
    password_box.submit()
    element = wait_and_get(driver, By.CSS_SELECTOR, ".confirm, .error")
    if element is None:
        raise RuntimeError("Could not login...")
    else:
        elem_class = element.get_attribute("class")
        if elem_class == "error":
            print(element.text)
            exit(1)
        else:
            print("Login successful!")


def login(driver: WebDriver, credentials: Optional[TalksCredentials] = None):
    url = get_talks_url(login_route)
    login_with(url, driver, credentials)


def login_and_return(
    driver: WebDriver, return_url: str, credentials: Optional[TalksCredentials] = None
):
    options = [("return_url", urllib.parse.quote(return_url, safe=""))]
    url = get_talks_url(login_route, options=options)
    login_with(url, driver, credentials)

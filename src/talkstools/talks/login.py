from dataclasses import dataclass
from typing import Optional
import urllib.parse
import requests
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from talkstools.auth import read_credentials

from talkstools.talks.start import driver_get, get_talks_url
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


def login_with_selenium_route(
    endpoint: str, driver: WebDriver, credentials: Optional[TalksCredentials] = None
) -> str:
    print("Logging in...")
    if credentials is None:
        talks_credentials = get_talks_credentials()
    else:
        talks_credentials = credentials
    driver_get(driver, endpoint)
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
            cookie = driver.get_cookie("_session_id")
            if cookie is None:
                raise RuntimeError("Could not get session cookie")
            return cookie["value"]


def login_with_selenium(
    driver: WebDriver, credentials: Optional[TalksCredentials] = None
) -> str:
    url = get_talks_url(login_route)
    return login_with_selenium_route(url, driver, credentials)


def login_with_selenium_and_return(
    driver: WebDriver, return_url: str, credentials: Optional[TalksCredentials] = None
) -> str:
    options = [("return_url", urllib.parse.quote(return_url, safe=""))]
    url = get_talks_url(login_route, options=options)
    return login_with_selenium_route(url, driver, credentials)


login_route = "/login/not_raven_login"


def login_with_requests(credentials: Optional[TalksCredentials] = None) -> str:
    if credentials is None:
        talks_credentials = get_talks_credentials()
    else:
        talks_credentials = credentials
    url = get_talks_url(login_route)
    data = {
        "email": talks_credentials.user,
        "password": talks_credentials.password,
        "commit": "Log+in",
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise RuntimeError("Could not log in")
    cookies = response.cookies.get_dict()
    session_id = cookies.get("_session_id")
    if session_id is None:
        raise RuntimeError("Could not get session id")
    return session_id

import urllib.parse
from outcome import Value
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from talkstools.talks.start import get_talks_url
from talkstools.talks.utils import fill_box, wait_and_get

login_route = "login/other_users"
invalid_route = "login/not_raven_login"


def login_with(endpoint: str, driver: WebDriver, user: str, password: str):
    print("Logging in...")
    driver.get(endpoint)
    fill_box(driver, By.ID, "email", user)
    password_box = fill_box(driver, By.ID, "password", password)
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


def login(driver: WebDriver, user: str, password: str):
    url = get_talks_url(login_route)
    login_with(url, driver, user, password)


def login_and_return(driver: WebDriver, return_url: str, user: str, password: str):
    options = [("return_url", urllib.parse.quote(return_url, safe=""))]
    url = get_talks_url(login_route, options=options)
    login_with(url, driver, user, password)

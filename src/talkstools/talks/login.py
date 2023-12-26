import urllib.parse
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from talkstools.talks.start import get_talks_url
from talkstools.talks.utils import fill_box

login_route = "login/other_users"

def login_with(endpoint: str, driver : WebDriver, user: str, password: str):
    driver.get(endpoint)
    fill_box(driver, By.ID, "email", user)
    password_box = fill_box(driver, By.ID, "password", password)
    password_box.submit()

def login(driver : WebDriver, user: str, password: str):
    url = get_talks_url(login_route)
    login_with(url, driver, user, password)

def login_and_return(driver : WebDriver, return_url : str, user : str, password: str):
    options = [("return_url", urllib.parse.quote(return_url, safe=''))]
    url = get_talks_url(login_route, options=options)
    login_with(url, driver, user, password)
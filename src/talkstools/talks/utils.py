from typing import Optional
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoAlertPresentException


def fill_box_if_not_none(
    driver: WebDriver, selector: str, value: str, content: Optional[str]
) -> Optional[WebElement]:
    if content is not None:
        return fill_box(driver, selector, value, content)
    else:
        return None


def fill_box(driver: WebDriver, selector: str, value: str, content: str) -> WebElement:
    box = wait_and_get(driver, selector, value)
    if box is None:
        raise RuntimeError("Box not found")
    else:
        box.clear()
        box.send_keys(content)
        return box


def wait_and_get(
    driver: WebDriver, selector: str, value: str, timeout: int = 30
) -> Optional[WebElement]:
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((selector, value))
        )
        try:
            driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        return element
    except Exception:
        return None

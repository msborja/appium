import pytest
import os
import allure

from appium.options.android import UiAutomator2Options
from selenium.webdriver.chrome.options import Options
from appium import webdriver as appium_webdriver
from selenium import webdriver as selenium_webdriver
from selene import browser
from dotenv import load_dotenv
from bg_spas_tests.utils import attach


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def context():
    return {}


@pytest.fixture(scope='session')
def mobile_driver():
    with allure.step('Configurate options'):
        user_name = os.getenv("USER_NAME")
        access_key = os.getenv("ACCESS_KEY")
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "11.0",
            "deviceName": "Google Pixel 4",
            "browserstack.timezone": 'Moscow',
            "app": "bs://d4de96da285707cefcb1f9e979074d8c9a171b42",
            'bstack:options': {
                "projectName": "bg_spas",
                "buildName": "build_1",
                "sessionName": "bs_spas_test",

                "userName": user_name,
                "accessKey": access_key
            }
        })
    driver = appium_webdriver.Remote('http://hub.browserstack.com/wd/hub',
                                     options=options)
    browser.config.driver = driver
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield driver

    attach.add_xml(browser)
    attach.add_screenshot(browser)
    attach.add_video_mobile(browser)

    browser.quit()


@pytest.fixture(scope='session')
def web_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options.capabilities.update(selenoid_capabilities)

    driver = selenium_webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options)
    browser.config.driver = driver
    browser.config.base_url = 'https://bg-dev.brealit.com'

    yield driver

    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_logs(browser)
    attach.add_video_web(browser)

    browser.quit()

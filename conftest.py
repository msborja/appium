import pytest
import os
import allure

from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser
from dotenv import load_dotenv
from utils import attach


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Configurate options'):
        user_name = os.getenv("USER_NAME")
        access_key = os.getenv("ACCESS_KEY")
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "11.0",
            "deviceName": "Google Pixel 4",

            "app": "bs://sample.app",

            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key
            }
        })



    browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub',
                                                 options=options)
    browser.config.timeout = float(os.getenv('timeout', '10.0'))


    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)
    attach.add_video(browser)

    with allure.step('Close app session'):
        browser.quit()

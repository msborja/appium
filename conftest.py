import os
import pytest

from dotenv import load_dotenv
from selene import Browser, Config
from appium import webdriver as appium_webdriver
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options
from appium.options.android import UiAutomator2Options
from bg_spas_collection.utils import attach
from bg_spas_collection.utils.attach import add_screenshot


@pytest.fixture(scope='session')
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def mobile_browser_init(load_env):
    user_name = os.getenv("USER_NAME")
    access_key = os.getenv("ACCESS_KEY")

    mobile_browser: Browser = None
    mobile_driver: appium_webdriver.Remote = None

    def _init():
        nonlocal mobile_browser, mobile_driver
        if mobile_driver is None:
            options_mobile = UiAutomator2Options().load_capabilities({
                "platformName": "android",
                "platformVersion": "11.0",
                "deviceName": "Google Pixel 4",
                "timezone": 'Moscow',
                "app": "bs://081d0ea196cf35675f23093215cf24b321216e08",
                'bstack:options': {
                    "projectName": "bg_spas",
                    "buildName": "mobile_spas_test",
                    "sessionName": "mobile_spas",
                    "timezone": 'Moscow',
                    "userName": user_name,
                    "accessKey": access_key
                }
            })
            mobile_driver = appium_webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options_mobile)
            mobile_browser = Browser(Config(driver=mobile_driver, timeout=float(os.getenv('timeout', '10.0'))))
        return mobile_browser, mobile_driver

    try:
        yield _init
    finally:
        if mobile_driver:
            try:
                attach.add_screenshot(mobile_browser)
                attach.add_xml(mobile_browser)
                attach.add_video_mobile(mobile_browser)
            except Exception as e:
                print(f"Failed to attach mobile browser artifacts: {e}")
            finally:
                mobile_driver.quit()


@pytest.fixture(scope="function")
def web_browser_init(load_env):
    user_name = os.getenv("USER_NAME")
    access_key = os.getenv("ACCESS_KEY")

    web_browser: Browser = None
    web_driver: selenium_webdriver.Remote = None

    def _init():
        nonlocal web_browser, web_driver
        if web_driver is None:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.capabilities.update({
                "os": "Windows",
                "osVersion": "10",
                "browserName": "Chrome",
                "browserVersion": "130.0",
                'bstack:options': {
                    "projectName": "bg_spas",
                    "buildName": "web_spas_test",
                    "sessionName": "web_spas",
                }
            })

            web_driver = selenium_webdriver.Remote(
                command_executor=f"https://{user_name}:{access_key}@hub.browserstack.com/wd/hub",
                options=options
            )
            web_browser = Browser(Config(driver=web_driver, timeout=float(os.getenv('timeout', '10.0'))))
        return web_browser, web_driver

    try:
        yield _init
    finally:
        if web_driver:
            try:
                add_screenshot(web_browser)
                attach.add_html(web_browser)
                attach.add_logs(web_browser)
                attach.add_video_web(web_browser)
            except Exception as e:
                print(f"Failed to attach web browser artifacts: {e}")
            finally:
                web_driver.quit()

import pytest
import os
import allure

from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser
from bg_spas_tests.utils import attach


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apk_path = os.path.join(current_dir, "resources", "bg_spas(2.1.1).apk")

    with allure.step('Configurate options'):
        options = UiAutomator2Options().load_capabilities({
            "platformName": "Android",
            "appium:platformVersion": "10",
            "appium:deviceName": "emulator-5554",
            "appium:app": apk_path,
            "appium:appPackage": "com.brealit.bg.spas",
            # "appium:appActivity": "com.brealit.bg.spas.MainActivity",
            "appium:automationName": "UiAutomator2",
            # "appium: ignoreHiddenApiPolicyError": True,
        })

    browser.config.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)
    attach.add_video(browser)

    with allure.step('Close app session'):
        browser.quit()

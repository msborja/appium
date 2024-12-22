import allure
import os

from time import sleep
from selene import be, browser
from dotenv import load_dotenv
from bg_spas_tests.data.codes import Codes
from appium.webdriver.common.appiumby import AppiumBy


class Authorization:
    def __init__(self):
        load_dotenv()
        self.user_name = os.getenv("USER_NAME")
        self.access_key = os.getenv("ACCESS_KEY")

    @allure.step('Closing allow access notification')
    def closing_allow_access_notification(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        allow_button = browser.element('(//android.widget.Button)[1]')
        if allow_button.matching(be.visible):
            allow_button.click()
        return self

    @allure.step('Select DEV server')
    def select_dev_server(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element((AppiumBy.ACCESSIBILITY_ID, "settings")).click()
        sleep(0.5)
        browser.element("//*[contains(@text, 'DEV server')]").click()
        return self

    @allure.step('Enter mobile phone')
    def enter_mobile_phone(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(3)
        browser.element("// android.widget.TextView[@text = 'ВХОД ДЛЯ СОТРУДНИКОВ']").click()
        browser.element((AppiumBy.CLASS_NAME, 'android.widget.EditText')).click().type('79139129200')
        # Решение для эмулятора:
        # browser.element((AppiumBy.CLASS_NAME, 'android.widget.EditText')).click()
        # os.system("adb shell input text '79139129200'")
        browser.element((AppiumBy.ACCESSIBILITY_ID, "ВХОД")).click()
        return self

    @allure.step('Type correct SMS code')
    def type_correct_sms_code(self, codes: Codes, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(2)
        for i, num in enumerate(codes.sms_code, start=1):
            browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click().type(f'{num}')
            # Решение для эмулятора:
            # browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click()
            # os.system(f'adb shell input text {num}')
        return self

    @allure.step('Type incorrect SMS code')
    def type_incorrect_sms_code(self, codes: Codes, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(2)
        for i, num in enumerate(codes.sms_code, start=1):
            browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click().type(f'{num}')
            # Решение для эмулятора:
            # browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click()
            # os.system(f'adb shell input text {num}')
        return self

    @allure.step('Setting a PIN code')
    def setting_pin_code(self, codes: Codes, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(2)
        for i, num in enumerate(codes.pin_code, start=1):
            browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click().type(f'{num}')
            # Решение для эмулятора:
            # browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click()
            # os.system(f'adb shell input text {num}')
        return self

    @allure.step('Type correct PIN code')
    def type_correct_pin_code(self, codes: Codes, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(2)
        for i, num in enumerate(codes.pin_code, start=1):
            browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click().type(f'{num}')
            # Решение для эмулятора:
            # browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click()
            # os.system(f'adb shell input text {num}')
        return self

    @allure.step('Type incorrect PIN code')
    def type_incorrect_pin_code(self, codes: Codes, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(2)
        for i, num in enumerate(codes.pin_code, start=1):
            browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click().type(f'{num}')
            # Решение для эмулятора:
            # browser.element(f'//android.widget.EditText[{i}]').should(be.visible).click()
            # os.system(f'adb shell input text {num}')
        return self

    @allure.step('Verifying successful authorization')
    def verifying_successful_authorization(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element((AppiumBy.ACCESSIBILITY_ID, 'СПАС')).should(be.visible)
        return self

    @allure.step('Verifying unsuccessful authorization')
    def verifying_unsuccessful_authorization(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element("// android.widget.TextView").should(be.visible)
        return self

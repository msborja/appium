from time import sleep
from allure import step
from selene import browser, be
from appium.webdriver.common.appiumby import AppiumBy

from bg_spas_tests.data.codes import Codes


class Authorization:
    with step('Closing allow access notification'):
        def closing_allow_access_notification(self):
            allow_button = browser.element('(//android.widget.Button)[1]')
            if allow_button.matching(be.visible):
                allow_button.click()
            return self

    with step('Select DEV server'):
        def select_dev_server(self):
            browser.element((AppiumBy.ACCESSIBILITY_ID, "settings")).click()
            browser.element("//*[contains(@text, 'DEV server')]").click()
            sleep(3)
            return self

    with step('Enter mobile phone'):
        def enter_mobile_phone(self):
            browser.element("// android.widget.TextView[@text = 'ВХОД ДЛЯ СОТРУДНИКОВ']").click()
            browser.element((AppiumBy.CLASS_NAME, 'android.widget.EditText')).should(be.visible).click()
            sleep(2)
            browser.element((AppiumBy.CLASS_NAME, 'android.widget.EditText')).should(be.enabled).type('79139129200')

            browser.element((AppiumBy.ACCESSIBILITY_ID, "ВХОД")).click()
            sleep(5)
            return self

    with step('Type correct SMS code'):
        def type_correct_sms_code(self, codes: Codes):
            for i, num in enumerate(codes.sms_code, start=1):
                browser.element(f'//android.widget.EditText[{i}]').should(be.visible).type(num)
            sleep(1)
            return self

    with step('Type incorrect SMS code'):
        def type_incorrect_sms_code(self, codes: Codes):
            for i, num in enumerate(codes.sms_code, start=1):
                browser.element(f'//android.widget.EditText[{i}]').type(num)
            sleep(1)
            return self

    with step('Setting a PIN code'):
        def setting_pin_code(self, codes: Codes):
            for i, num in enumerate(codes.pin_code, start=1):
                browser.element(f'//android.widget.EditText[{i}]').type(num)
            sleep(1)
            return self

    with step('Type correct PIN code'):
        def type_correct_pin_code(self, codes: Codes):
            for i, num in enumerate(codes.pin_code, start=1):
                browser.element(f'//android.widget.EditText[{i}]').type(num)
            sleep(1)
            return self

    with step('Type incorrect PIN code'):
        def type_incorrect_pin_code(self, codes: Codes):
            for i, num in enumerate(codes.pin_code, start=1):
                browser.element(f'//android.widget.EditText[{i}]').type(num)
            sleep(1)
            return self

    with step('Verifying successful authorization'):
        def verifying_successful_authorization(self):
            browser.element((AppiumBy.ACCESSIBILITY_ID, 'СПАС')).should(be.visible)
            return self

    with step('Verifying unsuccessful authorization'):
        def verifying_unsuccessful_authorization(self):
            browser.element("// android.widget.TextView").should(be.visible)
            return self


authorization = Authorization()

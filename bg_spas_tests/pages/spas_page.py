from time import sleep
import random
from allure import step
from selene import browser, have, be
from appium.webdriver.common.appiumby import AppiumBy
from bg_spas_tests.data.codes import Codes


class SPAS:
    with step('Open SPAS tab'):
        def open_spas(self):
            sleep(25)
            browser.element((AppiumBy.ACCESSIBILITY_ID, 'СПАС')).click()
            sleep(5)
            return self

    with step('Add SPAS card'):
        def add_spas_card(self):
            browser.element((AppiumBy.ACCESSIBILITY_ID, 'add')).click()
            sleep(3)
            return self

    with step('Closing allow access notification'):
        def closing_allow_access_notification(self):
            allow_button = browser.element('(//android.widget.Button)[1]')
            if allow_button.matching(be.visible):
                allow_button.click()
            sleep(1)
            return self

    with step('Fill SPAS card'):
        def fill_spas_card(self):
            browser.element('//android.view.View[@text="ОК"]').should(be.visible).click()

            with step('Filling "Organization" field'):
                browser.element('//android.widget.Spinner').click()

                dropdown_organizations = browser.all((AppiumBy.CLASS_NAME, 'android.widget.CheckedTextView'))
                random_index = random.randint(0, len(dropdown_organizations) - 1)
                random_organization = dropdown_organizations[random_index]
                random_organization.click()

            with step('Filling "Division" field'):
                browser.element('//android.view.View[@text="Подразделение *"]/following-sibling::*[1]').click()

                random_letter = random.choice('абвгдежзийклмнопрстуфхцчшщьыэюя')
                browser.element('//android.widget.EditText[@index="0"]').should(be.visible).click().type(random_letter)

                dropdown_division = browser.all((AppiumBy.CLASS_NAME, 'android.widget.ListView')).all(
                    (AppiumBy.CLASS_NAME, 'android.view.View'))
                random_choice_division = random.randint(0, len(dropdown_division) - 1)
                random_division = dropdown_division[random_choice_division]
                random_division.click()

                browser.element('//android.view.View[@text="Объект"]/following-sibling::*[1]').type('Объект')

                # type_card = browser.all((AppiumBy.CLASS_NAME,
                #                          '//android.view.View[@text="Вид карточки"]/following::android.view.View'))
                random_choice_type_card = random.randint(1, 3)
                random_element = browser.element(
                    f'//android.view.View[@text="Вид карточки"]/following-sibling::android.view.View[{random_choice_type_card}]')
                random_element.click()

            return self


spas = SPAS()

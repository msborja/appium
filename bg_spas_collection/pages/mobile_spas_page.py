import re
import os
import pytz
import allure
import random
import string

from time import sleep
from selene import be, browser
from datetime import datetime, timedelta
from selene.core.query import text
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MobileSpas:

    def __init__(self):
        self.card_number = None
        self.random_organization = None
        self.random_division = None
        self.random_object = None
        self.random_type_card = None
        self.random_participation = []
        self.random_description = None
        self.random_suggested = None
        self.random_measures = None
        self.random_name = None
        self.random_fix_date = None
        self.random_when_fix_date = None
        self.random_hazard_category = None
        self.random_damage_category = None
        self.random_damage_subcategory = None
        self.random_severity = None
        self.random_probability = None
        self.quantity_attachment = '4'

        self.timeout = 20

    @allure.step('Open SPAS tab')
    def open_spas_page(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(20)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'СПАС')).click()
        sleep(25)

        return self

    @allure.step('Add SPAS card')
    def add_spas_card(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element((AppiumBy.ACCESSIBILITY_ID, 'add')).click()
        sleep(3)

        return self

    @allure.step('Closing allow access notification')
    def closing_allow_access_notification(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        allow_button = browser.element('(//android.widget.Button)[1]')
        if allow_button.matching(be.visible):
            allow_button.click()
        sleep(1)

        return self

    @allure.step('Closing warning notification')
    def closing_warning_notification(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        sleep(1)
        browser.element('//android.widget.TextView[@text="ОК"]').should(be.enabled).click()

        return self

    @allure.step('Filling "Organization" field')
    def filling_organization_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.ListView/android.view.View[3]/android.view.View/android.view.View').click()

        dropdown_organizations = browser.all(
            '//android.widget.ListView//android.widget.CheckedTextView')
        sleep(2)
        random_index = random.randint(1, len(dropdown_organizations) - 1)
        random_organization = dropdown_organizations[random_index]
        self.random_organization = random_organization.get(text)

        random_organization.click()

        return self

    @allure.step('Filling "Division" field')
    def filling_division_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element('//android.widget.TextView[@text="Подразделение *"]/following-sibling::android.view.View[1]'
                        ).should(be.visible).click()

        random_letter = random.choice('абвгдежзийклмнопрстуфхцчшщьыэюя')

        browser.element('//android.widget.EditText[@index="0"]').should(be.visible).click().type(random_letter)
        dropdown_division = browser.all(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ListView")'
                                           '.instance(1)')).all((AppiumBy.CLASS_NAME, 'android.view.View'))

        if len(dropdown_division) == 0:
            browser.element('//android.widget.EditText[@index="0"]').clear()
            browser.element('//android.widget.EditText[@index="0"]').type('в')

        random_choice_division = random.randint(0, len(dropdown_division) - 1)
        random_dropdown_division = dropdown_division[random_choice_division]
        random_dropdown_division.click()

        division_field = (
            '//android.widget.TextView[@text="Подразделение *"]/following-sibling::*[1]//*[1]')
        division_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, division_field)))

        self.random_division = division_element.text

        return self

    @staticmethod
    @allure.step('Generate random text')
    def generate_random_text(length):
        characters = string.ascii_letters + string.digits
        random_text = ''.join(random.choices(characters, k=length))
        return random_text

    @allure.step('Filling "Object" field')
    def filling_object_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        self.random_object = MobileSpas.generate_random_text(15)
        browser.element('//android.widget.TextView[@text="Объект"]/following-sibling::*[1]'
                        ).type(self.random_object)

        return self

    @allure.step('Filling "Type card" field')
    def filling_type_card_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        random_choice_type_card = random.randint(1, 3)
        random_element = browser.element(
            f'//android.widget.TextView[@text="Вид карточки"]'
            f'/following-sibling::*[{random_choice_type_card}]//*[2]/*[1]')
        random_element.click()

        type_card_locator = (f'//android.widget.TextView[@text="Вид карточки"]'
                             f'/following-sibling::*[{random_choice_type_card}]//*[2]/*[1]')
        type_card_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, type_card_locator)))

        self.random_type_card = type_card_element.text

        return self

    @allure.step('Swipe')
    def swipe(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        screen_size = browser.config.driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.82
        end_y = screen_size['height'] * 0.2
        browser.config.driver.swipe(start_x, start_y, start_x, end_y)

        return self

    @allure.step('Filling "With participation" field')
    def filling_participation_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        available_indices = [4, 5, 6]
        random.shuffle(available_indices)
        selected_indices = available_indices[:random.randint(1, 3)]

        clicked_elements = []

        for index in selected_indices:
            element_locator = (f'//android.widget.ListView/android.view.View[{index}]'
                               f'/android.view.View/android.view.View[2]/*[1]')

            browser.element(element_locator).click()
            clicked_elements.append(element_locator)

        for locator in clicked_elements:
            element = WebDriverWait(browser.driver, self.timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            self.random_participation.append(element.text)

        return self

    @allure.step('Filling "Description" field')
    def filling_description_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        self.random_description = MobileSpas.generate_random_text(25)

        browser.element('//android.widget.TextView[@text="Описание *"]/following-sibling::*[1]'
                        ).type(self.random_description)
        sleep(1)

        return self

    @allure.step('Filling "Suggested" field')
    def filling_suggested_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        self.random_suggested = MobileSpas.generate_random_text(44)
        browser.element('//android.widget.TextView[@text="Предложено"]/following-sibling::*[1]'
                        ).type(self.random_suggested)
        sleep(1)

        return self

    @allure.step('Filling "Measures" field')
    def filling_measures_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        self.random_measures = MobileSpas.generate_random_text(50)
        browser.element('//android.widget.TextView[@text="Принятые меры"]/following-sibling::*[1]'
                        ).type(self.random_measures)
        sleep(1)

        return self

    @staticmethod
    @allure.step('Generate random name')
    def generate_random_name(length):
        characters = string.ascii_letters
        random_text = ' '.join(''.join(random.choices(characters, k=length)) for _ in range(3))
        return random_text

    @allure.step('Filling "Full name" filed')
    def filling_full_name_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        self.random_name = MobileSpas.generate_random_name(10)

        browser.element('//android.widget.TextView[@text="Ответственный за устранение (Ф.И.О.)"]'
                        '/following-sibling::*[1]').type(self.random_name)
        sleep(1)

        return self

    @allure.step('Filling "Fix date" field')
    def filling_fix_date_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element('//android.widget.TextView[@text="Срок устранения"]/following-sibling::*[1]').click()

        random_choice_date = random.randint(1, 25)
        browser.element(f'//android.view.View[@resource-id="android:id/month_view"]'
                        f'//android.view.View[{random_choice_date}]').click()
        browser.element((AppiumBy.ID, 'android:id/button1')).click()
        sleep(1)

        fix_date_locator = '//android.widget.TextView[@text="Срок устранения"]/following-sibling::*[1]'
        fix_date_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, fix_date_locator)))

        self.random_fix_date = fix_date_element.text

        return self

    @allure.step('Filling "When fix date" field')
    def filling_when_fix_date_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element('//android.widget.TextView[@text="Когда устранено"]/following-sibling::*[1]').click()

        random_choice_date = random.randint(1, 25)
        browser.element(f'//android.view.View[@resource-id="android:id/month_view"]'
                        f'//android.view.View[{random_choice_date}]').click()
        browser.element((AppiumBy.ID, 'android:id/button1')).click()
        sleep(1)

        when_fix_date_locator = '//android.widget.TextView[@text="Когда устранено"]/following-sibling::*[1]'
        when_fix_date_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, when_fix_date_locator)))

        self.random_when_fix_date = when_fix_date_element.text

        return self

    @allure.step('Filling "Hazard category" field')
    def filling_hazard_category_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.TextView[contains(@text, "Категория опасности")]/following-sibling::*[1]').click()
        sleep(1)
        dropdown_category = browser.all('//android.widget.ListView//android.widget.CheckedTextView')
        sleep(1)
        random_index = random.randint(1, len(dropdown_category) - 1)
        random_category = dropdown_category[random_index]
        random_category.click()
        sleep(1)

        hazard_category_locator = ('//android.widget.TextView[contains(@text,"Категория опасности")]'
                                   '/following-sibling::*[1]')
        hazard_category_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, hazard_category_locator)))

        self.random_hazard_category = hazard_category_element.text

        return self

    @allure.step('Filling "Damage category" field')
    def filling_damage_category_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.TextView[contains(@text, "Категория потенциального")]/following-sibling::*[1]'
        ).click()

        dropdown_category = browser.all('//android.widget.ListView//android.widget.CheckedTextView')
        sleep(1)
        random_index = random.randint(1, len(dropdown_category) - 1)
        random_category = dropdown_category[random_index]
        random_category.click()
        sleep(1)

        damage_category_locator = ('//android.widget.TextView[contains(@text, "Категория потенциального")]'
                                   '/following-sibling::*[1]')
        damage_category_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, damage_category_locator)))

        self.random_damage_category = damage_category_element.text

        return self

    @allure.step('Filling "Damage subcategory" field')
    def filling_damage_subcategory_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.TextView[contains(@text, "Подкатегория потенциального")]'
            '/following-sibling::*[1]').click()
        dropdown_category = browser.all('//android.widget.ListView//android.widget.CheckedTextView')
        sleep(1)
        random_index = random.randint(1, len(dropdown_category) - 1)
        random_category = dropdown_category[random_index]
        random_category.click()
        sleep(1)

        damage_subcategory_locator = ('//android.widget.TextView[contains(@text, "Подкатегория потенциального")'
                                      ']/following-sibling::*[1]')
        damage_subcategory_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, damage_subcategory_locator)))

        self.random_damage_subcategory = damage_subcategory_element.text

        return self

    @allure.step('Filling "Severity" field')
    def filling_severity_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.TextView[contains(@text, "Тяжесть последствий")]'
            '/following-sibling::*[1]').click()
        dropdown_category = browser.all('//android.widget.ListView//android.widget.CheckedTextView')
        sleep(1)
        random_index = random.randint(1, len(dropdown_category) - 1)
        random_category = dropdown_category[random_index]
        random_category.click()
        sleep(1)

        severity_locator = ('//android.widget.TextView[contains(@text, "Тяжесть последствий")]'
                            '/following-sibling::*[1]')
        severity_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, severity_locator)))

        self.random_severity = severity_element.text

        return self

    @allure.step('Filling "Probability" field')
    def filling_probability_field(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element(
            '//android.widget.TextView[contains(@text, "Вероятность")]'
            '/following-sibling::*[1]').click()
        dropdown_category = browser.all('//android.widget.ListView//android.widget.CheckedTextView')
        sleep(1)
        random_index = random.randint(1, len(dropdown_category) - 1)
        random_category = dropdown_category[random_index]
        random_category.click()
        sleep(1)

        probability_locator = ('//android.widget.TextView[contains(@text, "Вероятность")]'
                               '/following-sibling::*[1]')
        probability_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, probability_locator)))

        self.random_probability = probability_element.text

        return self

    @allure.step('Take a photo')
    def take_photo(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element('(//android.view.View[@resource-id="sheet_button"])[1]').click()
        sleep(1)
        allow_button = browser.element('(//android.widget.Button)[1]')
        if allow_button.matching(be.visible):
            allow_button.click()
        sleep(1)

        try:
            browser.element((AppiumBy.ID, 'com.google.android.GoogleCamera:id/shutter_button')).click()
            sleep(1)
            browser.element((AppiumBy.ID, 'com.google.android.GoogleCamera:id/shutter_button')).click()
        except Exception as e:
            print(e)
            browser.element('//android.widget.ImageView[@content-desc="Затвор"]').click()
            sleep(1)
            browser.element('//android.widget.ImageButton[@content-desc="Готово."]').click()

        return self

    # Решение для эмулятора
    # @allure.step('Attach a photo')
    # def attach_photo(self, mobile_browser):
    # browser.config.driver = mobile_browser.config.driver

    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     resource_dir = os.path.join(current_dir, "../../resources")
    #     resource_dir = os.path.abspath(resource_dir)
    #
    #     file_names = ['photo_1.jpg', 'photo_2.jpg', 'photo_3.jpeg']
    #
    #     for file_name in file_names:
    #         browser.element('(//android.view.View[@resource-id="sheet_button"])[2]').click()
    #         file_path = os.path.join(resource_dir, file_name)
    #         os.system(f'adb push {file_path} /sdcard/Download/')
    #         sleep(1)
    #         browser.element(
    #             '//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]').click()
    #         os.system(f'adb shell rm /sdcard/Download/{file_name}')
    #     return self

    @allure.step('Attach a photo')
    def attach_photo(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver
        sleep(2)

        browser.element('(//android.view.View[@resource-id="sheet_button"])[2]').click()

        try:
            photo_element = browser.element(
                '//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]'
            )

            if not photo_element.should(be.visible):
                mobile_browser.config.driver.back()
                self.quantity_attachment = '1'
            else:
                mobile_browser.config.driver.back()
                for _ in range(3):
                    browser.element('(//android.view.View[@resource-id="sheet_button"])[2]').click()
                    sleep(3)
                    photo_element.click()
                    sleep(1)
        except Exception:
            self.quantity_attachment = '1'
            mobile_browser.config.driver.back()

        return self

    @allure.step('Send card')
    def send_card_to_web(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element((AppiumBy.ACCESSIBILITY_ID, 'cloud_upload ОТПРАВИТЬ')).click()
        sleep(3)

        moscow_timezone = pytz.timezone('Europe/Moscow')
        current_datetime_now = datetime.now(moscow_timezone)
        current_datetime_str = current_datetime_now.strftime("%d.%m.%Y %H:%M")
        previous_datetime_str = (current_datetime_now - timedelta(minutes=1)).strftime("%d.%m.%Y %H:%M")

        card_element = (
            f'//android.view.View[contains(@content-desc, "{current_datetime_str}") or '
            f'contains(@content-desc, "{previous_datetime_str}")]'
        )

        element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, card_element)))
        content_desc = element.get_attribute('content-desc')
        sleep(1)
        match = re.search(r'# (\d+)', content_desc)
        sleep(4)
        if match:
            self.card_number = match.group(1)

        return self

    @allure.step('Save card to draft')
    def save_card_to_draft(self, mobile_browser):
        browser.config.driver = mobile_browser.config.driver

        browser.element((AppiumBy.ACCESSIBILITY_ID, 'cloud_upload ОТПРАВИТЬ')).click()

        return self

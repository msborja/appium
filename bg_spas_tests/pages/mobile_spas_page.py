import re
import allure
import random
import string

from time import sleep
from selene import browser, be
from datetime import datetime
from selene.core.query import text
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import mobile_driver


class MobileSpas:
    def __init__(self, mobile_driver):
        browser.config.driver = mobile_driver

    @allure.step('Open SPAS tab')
    def open_spas_page(self):
        sleep(25)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'СПАС')).click()
        sleep(13)

        return self

    @allure.step('Add SPAS card')
    def add_spas_card(self):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'add')).click()
        sleep(3)

        return self

    @allure.step('Closing allow access notification')
    def closing_allow_access_notification(self):
        allow_button = browser.element('(//android.widget.Button)[1]')
        if allow_button.matching(be.visible):
            allow_button.click()
        sleep(1)

        return self

    @allure.step('Closing warning notification')
    def closing_warning_notification(self):
        sleep(1)
        browser.element('//android.widget.TextView[@text="ОК"]').should(be.enabled).click()

        return self

    @allure.step('Filling "Organization" field')
    def filling_organization_field(self, context):
        browser.element('//android.widget.ListView/android.view.View[3]/android.view.View/android.view.View'
                        ).click()

        dropdown_organizations = browser.all(
            '//android.widget.ListView//android.widget.CheckedTextView')
        sleep(2)
        random_index = random.randint(1, len(dropdown_organizations) - 1)
        random_organization = dropdown_organizations[random_index]
        random_organization = random_organization.get(text)
        context["Organization"] = random_organization

        random_organization.click()

        return self

    @allure.step('Filling "Division" field')
    def filling_division_field(self, context):
        browser.element('//android.widget.TextView[@text="Подразделение *"]/following-sibling::android.view.View[1]'
                        ).should(be.visible).click()

        random_letter = random.choice('абвгдежзийклмнопрстуфхцчшщьыэюя')

        browser.element('//android.widget.EditText[@index="0"]').should(be.visible).click().type(random_letter)
        dropdown_division = browser.all(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ListView")'
                                           '.instance(1)')).all((AppiumBy.CLASS_NAME, 'android.view.View'))
        sleep(1)
        random_choice_division = random.randint(0, len(dropdown_division) - 1)
        random_dropdown_division = dropdown_division[random_choice_division]
        random_dropdown_division.click()

        division_field = (
            '//android.widget.TextView[@text="Подразделение *"]/following-sibling::*[1]//*[1]')
        division_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, division_field)))

        random_division = division_element.text
        context["Division"] = random_division

        return self

    @staticmethod
    @allure.step('Generate random text')
    def generate_random_text(length):
        characters = string.ascii_letters + string.digits
        random_text = ''.join(random.choices(characters, k=length))
        return random_text

    @allure.step('Filling "Object" field')
    def filling_object_field(self, context):
        random_object = mobileSpas.generate_random_text(15)
        context["Object"] = random_object
        browser.element('//android.widget.TextView[@text="Объект"]/following-sibling::*[1]'
                        ).type(random_object)

        return self

    @allure.step('Filling "Type card" field')
    def filling_type_card_field(self, context):
        random_choice_type_card = random.randint(1, 3)
        random_element = browser.element(
            f'//android.widget.TextView[@text="Вид карточки"]'
            f'/following-sibling::*[{random_choice_type_card}]//*[2]/*[1]')
        random_element.click()

        type_card_locator = (f'//android.widget.TextView[@text="Вид карточки"]'
                             f'/following-sibling::*[{random_choice_type_card}]//*[2]/*[1]')
        type_card_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, type_card_locator)))

        random_type_card = type_card_element.text
        context["Type_card"] = random_type_card

        return self

    @allure.step('Swipe')
    def swipe(self):
        screen_size = browser.config.driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.8
        end_y = screen_size['height'] * 0.2
        browser.config.driver.swipe(start_x, start_y, start_x, end_y)

        return self

    @allure.step('Filling "With participation" field')
    def filling_participation_field(self, context):
        available_indices = [4, 5, 6]
        random.shuffle(available_indices)
        selected_indices = available_indices[:random.randint(1, 3)]

        clicked_elements = []
        participation_values = []

        for index in selected_indices:
            element_locator = (f'//android.widget.ListView/android.view.View[{index}]'
                               f'/android.view.View/android.view.View[2]/*[1]')

            browser.element(element_locator).click()
            clicked_elements.append(element_locator)

        for locator in clicked_elements:
            element = WebDriverWait(browser.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            participation_values.append(element.text)

        context["Participation"] = participation_values

        return self

    @allure.step('Filling "Description" field')
    def filling_description_field(self, context):
        random_description = mobileSpas.generate_random_text(25)
        context["Description"] = random_description

        browser.element('//android.widget.TextView[@text="Описание *"]/following-sibling::*[1]'
                        ).type(random_description)
        sleep(1)

        return self

    @allure.step('Filling "Suggested" field')
    def filling_suggested_field(self, context):
        random_suggested = mobileSpas.generate_random_text(44)
        context["Suggested"] = random_suggested

        browser.element('//android.widget.TextView[@text="Предложено"]/following-sibling::*[1]'
                        ).type(random_suggested)
        sleep(1)

        return self

    @allure.step('Filling "Measures" field')
    def filling_measures_field(self, context):
        random_measures = mobileSpas.generate_random_text(50)
        context["Measures"] = random_measures

        browser.element('//android.widget.TextView[@text="Принятые меры"]/following-sibling::*[1]'
                        ).type(random_measures)
        sleep(1)

        return self

    @staticmethod
    @allure.step('Generate random name')
    def generate_random_name(length):
        characters = string.ascii_letters
        random_text = ' '.join(''.join(random.choices(characters, k=length)) for _ in range(3))
        return random_text

    @allure.step('Filling "Full name" filed')
    def filling_full_name_field(self, context):
        random_name = mobileSpas.generate_random_name(10)
        context["Full_name"] = random_name

        browser.element('//android.widget.TextView[@text="Ответственный за устранение (Ф.И.О.)"]'
                        '/following-sibling::*[1]').type(random_name)
        sleep(1)

        return self

    @allure.step('Filling "Fix date" field')
    def filling_fix_date_field(self, context):
        browser.element('//android.widget.TextView[@text="Срок устранения"]/following-sibling::*[1]').click()

        random_choice_date = random.randint(1, 25)
        browser.element(f'//android.view.View[@resource-id="android:id/month_view"]'
                        f'//android.view.View[{random_choice_date}]').click()
        browser.element((AppiumBy.ID, 'android:id/button1')).click()
        sleep(1)

        fix_date_locator = '//android.widget.TextView[@text="Срок устранения"]/following-sibling::*[1]'
        fix_date_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, fix_date_locator)))

        random_fix_date = fix_date_element.text
        context["Fix_date"] = random_fix_date

        return self

    @allure.step('Filling "When fix date" field')
    def filling_when_fix_date_field(self, context):
        browser.element('//android.widget.TextView[@text="Когда устранено"]/following-sibling::*[1]').click()

        random_choice_date = random.randint(1, 25)
        browser.element(f'//android.view.View[@resource-id="android:id/month_view"]'
                        f'//android.view.View[{random_choice_date}]').click()
        browser.element((AppiumBy.ID, 'android:id/button1')).click()
        sleep(1)

        when_fix_date_locator = '//android.widget.TextView[@text="Когда устранено"]/following-sibling::*[1]'
        when_fix_date_element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, when_fix_date_locator)))

        random_when_fix_date = when_fix_date_element.text
        context["When_fix_date"] = random_when_fix_date

        return self

    @allure.step('Filling "Hazard category" field')
    def filling_hazard_category_field(self, context):
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

        random_hazard_category = hazard_category_element.text
        context["Hazard_category"] = random_hazard_category

        return self

    @allure.step('Filling "Damage category" field')
    def filling_damage_category_field(self, context):
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

        random_damage_category = damage_category_element.text
        context["Damage_category"] = random_damage_category

        return self

    @allure.step('Filling "Damage subcategory" field')
    def filling_damage_subcategory_field(self, context):
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

        random_damage_subcategory = damage_subcategory_element.text
        context["Damage_subcategory"] = random_damage_subcategory

        return self

    @allure.step('Filling "Severity" field')
    def filling_severity_field(self, context):
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

        random_severity = severity_element.text
        context["Severity"] = random_severity

        return self

    @allure.step('Filling "Probability" field')
    def filling_probability_field(self, context):
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

        random_probability = probability_element.text
        context["Probability"] = random_probability

        return self

    @allure.step('Take a photo')
    def take_photo(self):
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
    # def attach_photo(self):
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
    def attach_photo(self):
        for _ in range(3):
            sleep(2)
            browser.element('(//android.view.View[@resource-id="sheet_button"])[2]').click()
            sleep(2)
            browser.element(
                '//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]').click()

        return self

    @allure.step('Send card')
    def send_card_to_web(self, context):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'cloud_upload ОТПРАВИТЬ')).click()
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M")
        card_element = f'//android.view.View[contains(@content-desc, "{current_datetime}")]'
        element = WebDriverWait(browser.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, card_element)))
        content_desc = element.get_attribute('content-desc')
        match = re.search(r'# (\d+)', content_desc)
        if match:
            card_number = match.group(1)
            context["Card_number"] = card_number

        return self

    @allure.step('Save card to draft')
    def save_card_to_draft(self):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'cloud_upload ОТПРАВИТЬ')).click()

        return self


mobileSpas = MobileSpas(mobile_driver)

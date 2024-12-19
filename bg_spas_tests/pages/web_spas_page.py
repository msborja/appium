import os
import re
import allure

from time import sleep
from selene import browser, be
from datetime import datetime
from selene.core.query import text
from selenium.common import NoSuchElementException
from conftest import context


class WebSpas:

    @allure.step('Authorization')
    def authorization(self):
        browser.open('/')
        browser.element('#emailField').type(os.getenv('LOGIN'))
        browser.element('#passField').type(os.getenv('PASS'))
        browser.element('[type="submit"]').click()

        return self

    @allure.step('Move to the SPAS module')
    def move_spas_module(self):
        browser.element("//span[contains(text(), 'СПАС')]").click()
        browser.element("//span[contains(text(), 'Карточки СПАС')]").click()

        return self

    @allure.step('Open SPAS card')
    def open_spas_card(self, context):
        card_number = context["Card_number"]
        sleep(5)
        browser.element(f'.row-id-{card_number}').should(be.clickable).double_click()

        return self

    @allure.step('Checking sync "Organization"')
    def checking_sync_organization(self, context):
        expected_organization = context["Organization"]

        try:
            browser.element('//*[@id="spas_cardsFormcompany_idWrapper"]/div/div/i').should(be.visible)

            actual_organization = browser.execute_script("""
                return document.evaluate(
                    '//*[@id="spas_cardsFormcompany_idWrapper"]/div/div/text()[2]',
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue?.nodeValue || null;
            """)
            actual_organization = actual_organization.lstrip(' -')

        except (NoSuchElementException, AssertionError):
            actual_organization = browser.element(
                '//*[@id="spas_cardsFormcompany_idWrapper"]/div/div').get(text)

        assert expected_organization == actual_organization, (
            f"Error: Expected organization '{expected_organization}' "
            f"does not match actual organization '{actual_organization}'.")

        return self

    @allure.step('Checking sync "Division"')
    def checking_sync_division(self, context):
        expected_division = context["Division"]

        actual_division_shortcut = browser.element('//*[@id="spas_cardsFormdidWrapper"]/div/div').get(text)
        actual_division_shortcut = actual_division_shortcut[-10:]

        browser.execute_script("window.open('/burgaz/departments', '_blank');")
        all_windows = browser.driver.window_handles
        browser.driver.switch_to.window(all_windows[-1])

        sleep(3)
        browser.element('[placeholder="Поиск"]').click().type(actual_division_shortcut)
        sleep(1)
        browser.element('//*[@id="departmentsList_Table"]/tbody/tr/td[5]').double_click()
        actual_division = browser.element('//*[@id="departmentsFormfullnameWrapper"]/div/div').get(text)

        assert expected_division.strip() == actual_division.strip(
        ), (f"Error: Expected division '{expected_division.strip()}' "
            f"does not match actual division '{actual_division.strip()}'.")

        browser.driver.switch_to.window(all_windows[0])

        return self

    @allure.step('Checking sync "Object"')
    def checking_sync_object(self, context):
        expected_object = context["Object"]

        browser.element('//*[@id="spas_cardsFormplaceWrapper"]/div/div/i').should(
            be.visible)
        actual_object = browser.execute_script("""
            var element = document.evaluate(
                '//*[@id="spas_cardsFormplaceWrapper"]/div/div/i',
                document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
            return element ? element.textContent : null;
        """)

        assert expected_object == actual_object.replace("Запись #", "").replace(" не найдена", "").strip(), (
            f"Error: Expected object '{expected_object}'"
            f" does not match actual object '{actual_object.replace("Запись #", "").replace(" не найдена", ""
                                                                                            ).strip()}'."
        )

        return self

    # @allure.step('Checking sync "Reporter/Observer"')
    #     def checking_sync_reporter(self):

    @allure.step('Checking sync "Type card"')
    def checking_sync_type_card(self, context):
        expected_type_card = context["Type_card"]
        actual_type_card = browser.element(
            '//*[@id="spas_cardsFormtypeWrapper"]/div/div').get(text)

        assert expected_type_card == actual_type_card, (
            f"Error: Expected type card '{expected_type_card}'"
            f" does not match actual type card '{actual_type_card}'."
        )

        return self

    @allure.step('Checking sync "With participation"')
    def checking_sync_participation(self, context):
        expected_participation = context["Participation"]

        actual_participation = browser.all(
            '//span[contains(@class, "checkbox-printedvalue-yes")]/ancestor::div[contains(@class, "control-group")]'
            '//span[contains(@class, "qform-prompt")]')

        actual_participation_texts = [participation.get(text) for participation in actual_participation]

        def normalize_data(data):
            return sorted([item.strip().lower() for item in data])

        normalized_expected_participation = normalize_data(expected_participation)
        normalized_actual_participation = normalize_data(actual_participation_texts)

        cleaned_actual_participation = list(filter(None, normalized_actual_participation))

        assert normalized_expected_participation == cleaned_actual_participation, (
            f"Error: Expected participation '{normalized_expected_participation}'"
            f" does not match actual participation '{normalized_actual_participation}'."
        )

        return self

    @allure.step('Checking sync "Description"')
    def checking_sync_description(self, context):
        expected_description = context["Description"]
        actual_description = browser.element(
            '//*[@id="spas_cardsFormdescriptionWrapper"]/div/div/p').get(text)

        assert expected_description == actual_description, (
            f"Error: Expected description '{expected_description}'"
            f" does not match actual description '{actual_description}'."
        )

        return self

    @allure.step('Checking sync "Suggested"')
    def checking_sync_suggested(self, context):
        expected_suggested = context["Suggested"]
        actual_suggested = browser.element(
            '//*[@id="spas_cardsFormtasks_suggestedWrapper"]/div/div/p').get(text)

        assert expected_suggested == actual_suggested, (
            f"Error: Expected suggested '{expected_suggested}'"
            f" does not match actual suggested '{actual_suggested}'."
        )

        return self

    @allure.step('Checking sync "Measures"')
    def checking_sync_measures(self, context):
        expected_measures = context["Measures"]
        actual_measures = browser.element(
            '//*[@id="spas_cardsFormtasks_completedWrapper"]/div/div/p').get(text)

        assert expected_measures == actual_measures, (
            f"Error: Expected measures '{expected_measures}'"
            f" does not match actual measures '{actual_measures}'."
        )

        return self

    @allure.step('Checking sync "Full name"')
    def checking_sync_full_name(self, context):
        expected_name = context["Full_name"]
        actual_name = browser.element(
            '//*[@id="spas_cardsFormresponsible_fioWrapper"]/div/div').get(text)

        assert expected_name == actual_name, (
            f"Error: Expected full name '{expected_name}'"
            f" does not match actual full name '{actual_name}'."
        )

        return self

    @allure.step('Checking sync "Fix date"')
    def checking_sync_fix_date(self, context):
        expected_fix_date = context["Fix_date"]
        actual_fix_date = browser.element(
            '//*[@id="spas_cardsFormdate_eliminationWrapper"]/div/div').get(text)
        actual_fix_date_unformatted = datetime.strptime(actual_fix_date, "%d.%m.%Y")
        actual_fix_date_formatted = actual_fix_date_unformatted.strftime("%Y-%m-%d")

        assert expected_fix_date == actual_fix_date_formatted, (
            f"Error: Expected fix date '{expected_fix_date}'"
            f" does not match actual fix date '{actual_fix_date_formatted}'."
        )

        return self

    @allure.step('Checking sync "When fix date"')
    def checking_sync_when_fix_date(self, context):
        expected_when_fix_date = context["When_fix_date"]
        actual_when_fix_date = browser.element(
            '//*[@id="spas_cardsFormdate_factWrapper"]/div/div').get(text)
        actual_when_fix_date_unformatted = datetime.strptime(actual_when_fix_date, "%d.%m.%Y")
        actual_when_fix_date_formatted = actual_when_fix_date_unformatted.strftime("%Y-%m-%d")

        assert expected_when_fix_date == actual_when_fix_date_formatted, (
            f"Error: Expected when fix date '{expected_when_fix_date}'"
            f" does not match actual when fix date '{actual_when_fix_date_formatted}'."
        )

        return self

    @allure.step('Checking sync "Hazard category"')
    def checking_sync_hazard_category(self, context):
        expected_hazard_category = context["Hazard_category"]
        actual_hazard_category = browser.element(
            '//*[@id="spas_cardsFormdangers_category_idWrapper"]/div/div').get(text)

        assert expected_hazard_category == actual_hazard_category, (
            f"Error: Expected hazard category '{expected_hazard_category}'"
            f" does not match actual hazard category '{actual_hazard_category}'."
        )

        return self

    @allure.step('Checking sync "Damage category"')
    def checking_sync_damage_category(self, context):
        expected_damage_category = context["Damage_category"]
        actual_damage_category = browser.element(
            '//*[@id="spas_cardsFormdamage_category_idWrapper"]/div/div').get(text)

        assert expected_damage_category == actual_damage_category, (
            f"Error: Expected damage category '{expected_damage_category}'"
            f" does not match actual damage category '{actual_damage_category}'."
        )

        return self

    @allure.step('Checking sync "Damage subcategory"')
    def checking_sync_damage_subcategory(self, context):
        expected_damage_subcategory = context["Damage_subcategory"]
        actual_damage_subcategory = browser.element(
            '//*[@id="spas_cardsFormdamage_sub_category_idWrapper"]/div/div').get(text)

        assert expected_damage_subcategory == actual_damage_subcategory, (
            f"Error: Expected damage subcategory '{expected_damage_subcategory}'"
            f" does not match actual damage subcategory '{actual_damage_subcategory}'."
        )

        return self

    @allure.step('Checking sync "Severity"')
    def checking_sync_severity(self, context):
        expected_severity = context["Severity"]
        actual_severity = browser.element(
            '//*[@id="spas_cardsFormaftereffect_valueWrapper"]/div/div').get(text)

        assert expected_severity == actual_severity, (
            f"Error: Expected severity '{expected_severity}'"
            f" does not match actual severity '{actual_severity}'."
        )

        return self

    @allure.step('Checking sync "Probability"')
    def checking_sync_probability(self, context):
        expected_probability = context["Probability"]
        actual_probability = browser.element(
            '//*[@id="spas_cardsFormprobability_valueWrapper"]/div/div').get(text)

        assert expected_probability == actual_probability, (
            f"Error: Expected probability '{expected_probability}'"
            f" does not match actual probability '{actual_probability}'."
        )

        return self

    @allure.step('Checking sync attachment')
    def checking_sync_attachment(self):
        expected_quantity_attachment = '4'
        browser.element("[id='spas_cardsFormfilesCaption']").click()
        text_element = browser.element(
            '//*[@id="spas_cardsfiles_embededList_Table_info"]').should(be.visible).get(text)
        sleep(1)
        match = re.search(r'Всего:\s*(\d+)', text_element)
        sleep(1)
        if match:
            actual_quantity_attachment = str(match.group(1))
        else:
            raise ValueError("No match found for 'Всего:' in the text")
        assert expected_quantity_attachment == actual_quantity_attachment, (
            f"Error: Expected attachment '{expected_quantity_attachment}'"
            f" does not match actual attachment '{actual_quantity_attachment}'."
        )

        return self

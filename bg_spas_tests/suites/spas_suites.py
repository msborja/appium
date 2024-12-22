import allure
import os

from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options

from bg_spas_tests.pages.authorization_page import Authorization
from bg_spas_tests.pages.mobile_spas_page import MobileSpas
from bg_spas_tests.pages.web_spas_page import WebSpas
from bg_spas_tests.data.codes import Codes


class SpasSuites:

    @allure.step('Authorize in mobile app')
    def authorize_in_mobile_app(self, mobile_browser):
        authorization = Authorization()
        codes = Codes(sms_code=['9', '2', '0', '0'], pin_code=['1', '2', '3', '4'])
        (authorization
         .closing_allow_access_notification(mobile_browser)
         .select_dev_server(mobile_browser)
         .enter_mobile_phone(mobile_browser)
         .type_correct_sms_code(codes, mobile_browser)
         .type_correct_pin_code(codes, mobile_browser)
         .setting_pin_code(codes, mobile_browser)
         .verifying_successful_authorization(mobile_browser))

    @allure.step('Send SPAS card in mobile app')
    def send_spas_card_in_mobile_app(self, mobile_browser):
        mobile_spas = MobileSpas()
        (mobile_spas
         .open_spas_page(mobile_browser)
         .add_spas_card(mobile_browser)
         .closing_allow_access_notification(mobile_browser)
         .closing_warning_notification(mobile_browser)
         .filling_organization_field(mobile_browser)
         .filling_division_field(mobile_browser)
         .filling_object_field(mobile_browser)
         .filling_type_card_field(mobile_browser)
         .swipe(mobile_browser)
         .filling_participation_field(mobile_browser)
         .filling_description_field(mobile_browser)
         .filling_suggested_field(mobile_browser)
         .filling_measures_field(mobile_browser)
         .swipe(mobile_browser)
         .filling_full_name_field(mobile_browser)
         .filling_fix_date_field(mobile_browser)
         .filling_when_fix_date_field(mobile_browser)
         .filling_hazard_category_field(mobile_browser)
         .filling_damage_category_field(mobile_browser)
         .filling_damage_subcategory_field(mobile_browser)
         .swipe(mobile_browser)
         .filling_severity_field(mobile_browser)
         .filling_probability_field(mobile_browser)
         .swipe(mobile_browser)
         .take_photo(mobile_browser)
         .attach_photo(mobile_browser)
         .send_card_to_web(mobile_browser))
        return mobile_spas

    @allure.step('Verify SPAS card in web app')
    def verify_spas_card_in_web_app(self, web_driver, mobile_spas):
        web_spas = WebSpas()
        (web_spas
         .authorization(web_driver)
         .move_spas_module(web_driver)
         .open_spas_card(mobile_spas, web_driver)
         .checking_sync_organization(mobile_spas, web_driver)
         .checking_sync_division(mobile_spas, web_driver)
         .checking_sync_object(mobile_spas, web_driver)
         .checking_sync_type_card(mobile_spas, web_driver)
         .checking_sync_participation(mobile_spas, web_driver)
         .checking_sync_description(mobile_spas, web_driver)
         .checking_sync_suggested(mobile_spas, web_driver)
         .checking_sync_measures(mobile_spas, web_driver)
         .checking_sync_full_name(mobile_spas, web_driver)
         .checking_sync_fix_date(mobile_spas, web_driver)
         .checking_sync_when_fix_date(mobile_spas, web_driver)
         .checking_sync_hazard_category(mobile_spas, web_driver)
         .checking_sync_damage_category(mobile_spas, web_driver)
         .checking_sync_damage_subcategory(mobile_spas, web_driver)
         .checking_sync_severity(mobile_spas, web_driver)
         .checking_sync_probability(mobile_spas, web_driver)
         .checking_sync_attachment(web_driver))

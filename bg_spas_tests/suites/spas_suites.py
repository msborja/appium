import allure
from bg_spas_tests.pages.authorization_page import Authorization
from bg_spas_tests.pages.mobile_spas_page import MobileSpas
from bg_spas_tests.pages.web_spas_page import WebSpas
from bg_spas_tests.data.codes import Codes
from conftest import mobile_driver, web_driver


class SpasSuites:
    def __init__(self, context, mobile_driver, web_driver):
        self.context = context
        self.authorization = Authorization(mobile_driver)
        self.mobile_spas = MobileSpas(mobile_driver)
        self.web_spas = WebSpas(web_driver)

    @allure.step('Authorize in mobile app')
    def authorize_in_mobile_app(self):
        codes = Codes(sms_code=['9', '2', '0', '0'], pin_code=['1', '2', '3', '4'])
        (self.authorization
         .closing_allow_access_notification()
         .select_dev_server()
         .enter_mobile_phone()
         .type_correct_sms_code(codes)
         .type_correct_pin_code(codes)
         .setting_pin_code(codes)
         .verify_authorization())

    @allure.step('Send SPAS card in mobile app')
    def send_spas_card_in_mobile_app(self):
        (self.mobile_spas
         .open_spas_page()
         .add_spas_card()
         .closing_allow_access_notification()
         .closing_warning_notification()
         .filling_organization_field(self.context)
         .filling_division_field(self.context)
         .filling_object_field(self.context)
         .filling_type_card_field(self.context)
         .swipe()
         .filling_participation_field(self.context)
         .filling_description_field(self.context)
         .filling_suggested_field(self.context)
         .filling_measures_field(self.context)
         .swipe()
         .filling_full_name_field(self.context)
         .filling_fix_date_field(self.context)
         .filling_when_fix_date_field(self.context)
         .filling_hazard_category_field(self.context)
         .filling_damage_category_field(self.context)
         .filling_damage_subcategory_field(self.context)
         .swipe()
         .filling_severity_field(self.context)
         .filling_probability_field(self.context)
         .swipe()
         .take_photo()
         .attach_photo()
         .send_card_to_web(self.context))

    @allure.step('Verify SPAS card in web app')
    def verify_spas_card_in_web_app(self):
        (self.web_spas
         .authorization()
         .move_spas_module()
         .open_spas_card(self.context)
         .checking_sync_organization(self.context)
         .checking_sync_division(self.context)
         .checking_sync_object(self.context)
         .checking_sync_type_card(self.context)
         .checking_sync_participation(self.context)
         .checking_sync_description(self.context)
         .checking_sync_suggested(self.context)
         .checking_sync_measures(self.context)
         .checking_sync_full_name(self.context)
         .checking_sync_fix_date(self.context)
         .checking_sync_when_fix_date(self.context)
         .checking_sync_hazard_category(self.context)
         .checking_sync_damage_category(self.context)
         .checking_sync_damage_subcategory(self.context)
         .checking_sync_severity(self.context)
         .checking_sync_probability(self.context)
         .checking_sync_attachment())

import allure
from bg_spas_tests.pages.authorization_page import Authorization
from bg_spas_tests.pages.mobile_spas_page import MobileSpas
from bg_spas_tests.pages.web_spas_page import WebSpas
from bg_spas_tests.data.codes import Codes
from conftest import mobile_driver, web_driver


class SpasSuites:
    def __init__(self, mobile_driver, web_driver):
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
         .filling_organization_field()
         .filling_division_field()
         .filling_object_field()
         .filling_type_card_field()
         .swipe()
         .filling_participation_field()
         .filling_description_field()
         .filling_suggested_field()
         .filling_measures_field()
         .swipe()
         .filling_full_name_field()
         .filling_fix_date_field()
         .filling_when_fix_date_field()
         .filling_hazard_category_field()
         .filling_damage_category_field()
         .filling_damage_subcategory_field()
         .swipe()
         .filling_severity_field()
         .filling_probability_field()
         .swipe()
         .take_photo()
         .attach_photo()
         .send_card_to_web())

    @allure.step('Verify SPAS card in web app')
    def verify_spas_card_in_web_app(self):
        (self.web_spas
         .authorization()
         .move_spas_module()
         .open_spas_card()
         .checking_sync_organization()
         .checking_sync_division()
         .checking_sync_object()
         .checking_sync_type_card()
         .checking_sync_participation()
         .checking_sync_description()
         .checking_sync_suggested()
         .checking_sync_measures()
         .checking_sync_full_name()
         .checking_sync_fix_date()
         .checking_sync_when_fix_date()
         .checking_sync_hazard_category()
         .checking_sync_damage_category()
         .checking_sync_damage_subcategory()
         .checking_sync_severity()
         .checking_sync_probability()
         .checking_sync_attachment())

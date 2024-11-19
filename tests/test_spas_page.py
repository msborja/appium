from bg_spas_tests.pages.authorization_page import authorization
from bg_spas_tests.pages.spas_page import spas
from bg_spas_tests.data.codes import Codes

import allure


@allure.story('')
def test_fill_spas_card():
    codes = Codes(
        sms_code=['9', '2', '0', '0'],
        pin_code=['1', '2', '3', '4']
    )
    (authorization.closing_allow_access_notification().select_dev_server().enter_mobile_phone().type_correct_sms_code(codes).setting_pin_code(
        codes).type_correct_pin_code(codes).verifying_successful_authorization())
    (spas.open_spas().add_spas_card().closing_allow_access_notification().fill_spas_card())

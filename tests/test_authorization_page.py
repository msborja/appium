import allure
from bg_spas_tests.pages.authorization_page import authorization
from bg_spas_tests.data.codes import Codes


@allure.story('Successful authorization')
def test_successful_authorization(mobile_driver):
    codes = Codes(
        sms_code=['9', '2', '0', '0'],
        pin_code=['1', '2', '3', '4']
    )
    authorization.closing_allow_access_notification()
    authorization.select_dev_server()
    authorization.enter_mobile_phone()
    authorization.type_correct_sms_code(codes).setting_pin_code(codes).type_correct_pin_code(codes)
    authorization.verifying_successful_authorization()


@allure.story('Unsuccessful authorization')
def test_unsuccessful_authorization(mobile_driver):
    codes = Codes(
        sms_code=['4', '9', '1', '3'],
        pin_code=['1', '2', '3', '4']
    )
    authorization.closing_allow_access_notification()
    authorization.select_dev_server()
    authorization.enter_mobile_phone()
    authorization.type_incorrect_sms_code(codes).type_incorrect_sms_code(codes).type_incorrect_sms_code(
        codes).type_incorrect_sms_code(codes).type_incorrect_sms_code(codes)
    authorization.verifying_unsuccessful_authorization()

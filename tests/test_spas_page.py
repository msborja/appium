import allure
from bg_spas_tests.suites.spas_suites import SpasSuites


@allure.story('Full SPAS card test')
def test_full_spas_card(mobile_driver, web_driver, context):
    spas_suites = SpasSuites(mobile_driver, web_driver)
    spas_suites.authorize_in_mobile_app()
    spas_suites.send_spas_card_in_mobile_app()
    spas_suites.verify_spas_card_in_web_app()



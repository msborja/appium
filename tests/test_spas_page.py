import allure
from bg_spas_tests.suites.spas_suites import SpasSuites


@allure.story('Full SPAS card test')
def test_full_spas_card(mobile_browser_init, web_browser_init):
    spas_suites = SpasSuites()

    with allure.step("Authorize in mobile app"):
        mobile_browser, mobile_driver = mobile_browser_init()
        spas_suites.authorize_in_mobile_app(mobile_browser)

    with allure.step("Send SPAS card in mobile app"):
        mobile_spas = spas_suites.send_spas_card_in_mobile_app(mobile_browser)

    with allure.step("Verify SPAS card in web app"):
        web_browser, web_driver = web_browser_init()
        spas_suites.verify_spas_card_in_web_app(web_driver, mobile_spas)

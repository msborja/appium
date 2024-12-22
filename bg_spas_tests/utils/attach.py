import os
import allure
import requests
import logging

from allure_commons.types import AttachmentType
from dotenv import load_dotenv

load_dotenv()
user_name = os.getenv("USER_NAME")
access_key = os.getenv("ACCESS_KEY")
attach_enabled = os.getenv("ATTACH_ENABLED", "true").lower() == "true"
logger = logging.getLogger(__name__)


def add_screenshot(browser):
    if not attach_enabled:
        return
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png,
                  name='screenshot',
                  attachment_type=allure.attachment_type.PNG)


def add_xml(browser):
    if not attach_enabled:
        return
    xml_dump = browser.driver.page_source
    allure.attach(body=xml_dump,
                  name='screen xml dump',
                  attachment_type=allure.attachment_type.XML)


def add_video_mobile(browser):
    if not attach_enabled:
        return
    try:
        browserstack_session = requests.get(
            url=f'https://api.browserstack.com/app-automate/sessions/{browser.driver.session_id}.json',
            auth=(user_name, access_key),
            timeout=10).json()
        video_url = browserstack_session['automation_session']['video_url']

        allure.attach(
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>',
            name='video_recording_mobile.html',
            attachment_type=allure.attachment_type.HTML,
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get BrowserStack video URL: {e}")


def add_logs(browser):
    if not attach_enabled:
        return
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs.txt', AttachmentType.TEXT)


def add_html(browser):
    if not attach_enabled:
        return
    html = browser.driver.page_source
    allure.attach(html, 'page_source.html', AttachmentType.HTML)


def add_video_web(browser):
    if not attach_enabled:
        return
    try:
        browserstack_session = requests.get(
            url=f'https://api.browserstack.com/automate/sessions/{browser.driver.session_id}.json',
            auth=(user_name, access_key),
            timeout=10).json()
        video_url = browserstack_session['automation_session']['video_url']

        allure.attach(
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>',
            name='video_recording.html',
            attachment_type=allure.attachment_type.HTML,
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get BrowserStack video URL: {e}")

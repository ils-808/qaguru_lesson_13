from typing import Literal

import pytest
import pydantic_settings

from utils import attach
from utils.resource_handler import path
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selene import browser

BrowserType = Literal['chrome', 'firefox', 'edge']


class Configure(pydantic_settings.BaseSettings):
    browser: BrowserType = 'chrome'
    version: str = '119'
    height: str = '1080'
    width: str = '1920'
    base_url: str = 'https://todomvc.com/examples/knockoutjs/'
    run_remote: bool = False


config = Configure(_env_file=path('.env'))


@pytest.fixture(scope='function', autouse=True)
def configure_browser():
    options = Options()
    if config.run_remote:
        selenoid_capabilities = {
            'browserName': config.browser,
            'browserVersion': config.version,
            'selenoid:options': {
                'enableVNC': True,
                'enableVideo': True
            }
        }
        options.capabilities.update(selenoid_capabilities)
        options.add_argument(f'--window-size={config.width},{config.height}')

        driver = webdriver.Remote(
            command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
            options=options
        )
        browser.config.driver = driver
    else:
        browser.config.driver_name = config.browser
        options.add_argument('--ignore-certificate-errors')
        browser.config.driver_options = options
        browser.config.window_width = config.width
        browser.config.window_height = config.height

    browser.config.base_url = config.base_url

    yield

    attach.add_screenshot(browser)
    attach.add_html(browser)
    if config.browser == 'chrome':
        attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()

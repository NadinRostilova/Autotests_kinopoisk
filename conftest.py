import time
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils.api_client import KinopoiskAPIClient
from config.api_config import API_CONFIG
from config.test_data import TestData
from selenium.common.exceptions import TimeoutException

@pytest.fixture(scope="session")
def api_client():
    return KinopoiskAPIClient(API_CONFIG["base_url"], API_CONFIG["api_key"])

@pytest.fixture(scope="session", autouse=True)
def chrome_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(TestData.BASE_URL)
    # Просто ждём 20 секунд, чтобы вы успели решить капчу и закрыть окна
    time.sleep(20)

    yield driver
    driver.quit()

@pytest.fixture
def auth_page(chrome_driver):
    from pages.auth_page import AuthPage
    return AuthPage(chrome_driver)

@pytest.fixture
def main_page(chrome_driver):
    from pages.main_page import MainPage
    return MainPage(chrome_driver)



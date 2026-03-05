from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class MainPage(BasePage):
    SEARCH_INPUT = (By.XPATH, "//input[@name='kp_query']")
    SEARCH_ICON = (By.CSS_SELECTOR, "button[type='submit']")  
    RESULT_ITEMS = (By.CSS_SELECTOR, "a[data-type='film']")
    MAIN_MENU = (By.XPATH, "//nav[@data-tid='e500879d']")
    TV_CHANNELS_ITEM = (
        By.XPATH,
        "//nav[@data-tid='e500879d']//a[.//span[text()='Телеканалы']]"
    )
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def is_mainmenu_loaded(self):
        """Проверяет, что главное меню загрузилось на странице"""
        try:
            self.wait.until(EC.presence_of_element_located(self.MAIN_MENU))
            return True
        except TimeoutException:
            return False

    def click_tv_channels(self):
        """Кликает по пункту «Телеканалы» в главном меню"""
        tv_button = self.wait.until(
            EC.element_to_be_clickable(self.TV_CHANNELS_ITEM)
        )
        tv_button.click()


    def get_first_search_result(self):
        """Возвращает первый результат поиска"""
        return self.wait.until(
            EC.element_to_be_clickable(self.RESULT_ITEMS)
        )

    def wait_for_movie_page_load(self):
        """Ожидает загрузки страницы фильма"""
        self.wait.until(EC.presence_of_element_located(self.MOVIE_TITLE_ON_PAGE))

    def search_movie(self, query: str):
        """Вводит поисковый запрос и запускает поиск."""
        self.input_text(self.SEARCH_INPUT, query)
        # Нажимаем кнопку поиска
        self.click_element(self.SEARCH_ICON)


    def is_mainmenu_loaded(self, timeout=30):
        """Проверяет, что главное меню загрузилось на странице"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.MAIN_MENU)
            )
            return True
        except TimeoutException:
            return False

    def click_tv_channels(self, timeout=30):  
        """Кликает по пункту «Телеканалы» в главном меню"""
        tv_button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.TV_CHANNELS_ITEM)
        )
        tv_button.click()

    def wait_for_tv_page_load(self, timeout=30):
        """Ожидает загрузки страницы телеканалов и проверяет URL"""
        WebDriverWait(self.driver, timeout).until(EC.url_contains("/channels"))
        return "/channels" in self.driver.current_url    
    
    
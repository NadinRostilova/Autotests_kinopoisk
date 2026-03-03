from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):
    # Локаторы элементов
    SEARCH_INPUT = (By.NAME, "kp_query")
    SEARCH_ICON = (By.CSS_SELECTOR, "button[type='submit']")  # Можно и так, если кнопка поиска - submit
    RESULT_ITEMS = (By.XPATH, "//p[@class='name']/a")  # Все результаты поиска

    def search_movie(self, query: str):
        """Вводит поисковый запрос и запускает поиск."""
        self.input_text(self.SEARCH_INPUT, query)
        # Нажимаем кнопку поиска
        self.click_element(self.SEARCH_ICON)
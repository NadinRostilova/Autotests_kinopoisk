from .base_page import BasePage
from selenium.webdriver.common.by import By

class AuthPage(BasePage):
    PHONE_INPUT = (By.NAME, "phone")
    SEND_CODE_BUTTON = (By.XPATH, "//button[contains(text(), 'Получить код')]")
    CODE_INPUT = (By.NAME, "code")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")


    def enter_phone(self, phone_number: str):
        """Вводит номер телефона.

        Args:
            phone_number (str): номер телефона для ввода
        """
        self.input_text(self.PHONE_INPUT, phone_number)

    def click_send_code(self):
        """Нажимает кнопку 'Получить код'."""
        self.click_element(self.SEND_CODE_BUTTON)

    def enter_code(self, code: str):
        """Вводит код подтверждения.

        Args:
            code (str): код подтверждения
        """
        self.input_text(self.CODE_INPUT, code)

    def submit_auth(self):
        """Подтверждает авторизацию."""
        self.click_element(self.SUBMIT_BUTTON)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        element = self.find_element(locator)
        element.click()

    def input_text(self, locator, text):
        input_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        input_element.clear()
        input_element.send_keys(text)
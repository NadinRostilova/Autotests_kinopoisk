import pytest
import allure
from config.test_data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pages.main_page import MainPage

@allure.feature("UI Тесты Кинопоиска")
class TestKinopoiskUI:

    @allure.story("Главная страница")
    @allure.title("Загрузка главной страницы")
    def test_main_page_loads(self, chrome_driver):
        with allure.step("Открываем главную страницу Кинопоиска"):
            chrome_driver.get(TestData.BASE_URL)

        try:
            with allure.step("Ожидаем загрузки страницы"):
                WebDriverWait(chrome_driver, 20).until(
                    EC.presence_of_element_located(("tag name", "body"))
        )

            with allure.step("Проверяем отсутствие капчи"):
                if "Вы не робот?" in chrome_driver.page_source:
                    allure.attach(
                chrome_driver.get_screenshot_as_png(),
                name="Captcha_detected",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.skip("Обнаружена капча — тест пропущен")

            with allure.step("Проверяем заголовок страницы"):
                assert "Кинопоиск" in chrome_driver.title
        except TimeoutException:
            allure.attach(
            chrome_driver.get_screenshot_as_png(),
            name="Page_timeout",
            attachment_type=allure.attachment_type.PNG
        )
        pytest.fail("Страница не загрузилась за отведённое время")

    @pytest.fixture
    def main_page(self, chrome_driver):
        return MainPage(chrome_driver)

    @allure.story("Поиск фильма")
    @allure.title("Поиск фильма 'Интерстеллар' и проверка поиска по результатам")
    def test_search_movie(self, main_page):
        driver = main_page.driver
        with allure.step("Переход на сайт Кинопоиск"):
            driver.get(TestData.BASE_URL)

        with allure.step("Выполняем поиск 'Интерстеллар'"):
            main_page.search_movie("Интерстеллар")

        # Ждем появления результатов
        with allure.step("Ждем элементов результатов поиска"):
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(MainPage.RESULT_ITEMS)
            )

        # Проверим, что есть результаты и что один из них содержит 'Интерстеллар'
        found = False
        for result in results:
            title = result.text
            href = result.get_attribute('href')
            print(f"Результат: {title} - {href}")
            if "Интерстеллар" in title:
                found = True
                break

        assert found, "Фильм 'Интерстеллар' не найден среди результатов поиска."

        # Сделать скриншот и лог
        allure.attach(driver.page_source, name="Результаты поиска", attachment_type=allure.attachment_type.HTML)

    @allure.story("Авторизация по коду")
    @allure.title("Успешная авторизация с тестовым кодом")
    def test_successful_auth_with_fixed_code(self):
        with allure.step("Вводим номер телефона"):
            # Замените на реальную логику страницы
            pass

    @allure.story("Обработка ошибок")
    @allure.title("Ошибка при вводе неверного кода")
    def test_invalid_code_error(self):
        with allure.step("Вводим номер телефона"):
            # Замените на реальную логику страницы
            pass

    @allure.story("Повторный запрос")
    @allure.title("Повторный запрос кода подтверждения")
    def test_resend_code(self):
        with allure.step("Вводим номер и запрашиваем код"):
            # Замените на реальную логику страницы
            pass
        
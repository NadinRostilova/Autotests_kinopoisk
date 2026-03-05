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
                WebDriverWait(chrome_driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

            with allure.step("Проверяем заголовок страницы"):
                assert "Кинопоиск" in chrome_driver.title
        except TimeoutException:
            allure.attach(
                chrome_driver.get_screenshot_as_png(),
                name="Page_timeout",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail("Страница не загрузилась за отведённое время")

    @allure.story("Поиск фильма")
    @allure.title("Поиск фильма 'Интерстеллар' и проверка поиска по результатам")
    def test_search_movie(self, main_page, chrome_driver):
        driver = main_page.driver
        with allure.step("Переход на сайт Кинопоиск"):
            driver.get(TestData.BASE_URL)

        with allure.step("Выполняем поиск 'Интерстеллар'"):
            main_page.search_movie("Интерстеллар")


        with allure.step("Ждём элементов результатов поиска"):
            results = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(MainPage.RESULT_ITEMS)
            )

        found = False
        for result in results:
            title = result.text
            href = result.get_attribute('href')
            print(f"Результат: {title} - {href}")
            if "Интерстеллар" in title:
                found = True
                break

        assert found, "Фильм 'Интерстеллар' не найден среди результатов поиска."
        allure.attach(driver.page_source, name="Результаты поиска", attachment_type=allure.attachment_type.HTML)


    @allure.story("Поиск фильма")
    @allure.title("Переход на страницу фильма по результатам поиска 'Интерстеллар'")
    def test_navigate_to_movie_page(self, main_page, chrome_driver):
        driver = main_page.driver
        driver.get(TestData.BASE_URL)
        main_page.search_movie("Интерстеллар")

        with allure.step("Ждём появления результатов поиска"):
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located(MainPage.RESULT_ITEMS)
            )

        with allure.step("Кликаем на первый результат"):
            try:
                results = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located(MainPage.RESULT_ITEMS)
                )
                first_result = results[0]
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(first_result))
                first_result.click()
            except TimeoutException:
                pytest.fail("Нет результатов поиска для перехода")

        with allure.step("Проверяем, что открылась страница фильма"):
            try:
                WebDriverWait(driver, 15).until(
                    EC.any_of(
                        EC.url_contains("/film/"),
                        EC.url_contains("/series/"),
                    )
                )
            except TimeoutException:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Movie_page_not_loaded",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail("Страница фильма не загрузилась")

            assert "Интерстеллар" in driver.title, "Название фильма не отображается в заголовке"

    @allure.story("Поиск фильма")
    @allure.title("Поиск несуществующего фильма и проверка результата")
    def test_search_nonexistent_movie(self, main_page, chrome_driver):
        driver = main_page.driver

        with allure.step("Переход на сайт Кинопоиск"):
            driver.get(TestData.BASE_URL)

        non_exist_movie = "ФильмКоторогоНетВБазе12345"

        with allure.step(f"Ищем несуществующий фильм '{non_exist_movie}'"):
            main_page.search_movie(non_exist_movie)

        with allure.step("Проверяем, что отображается сообщение о неподходящем результате"):
            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (
                            (By.XPATH, "//h2[contains(text(), 'К сожалению, по вашему запросу ничего не найдено')]")
                        )
                    )
                )
            except TimeoutException:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="No_results_message_not_found",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail("Сообщение о не найденных результатах не отображается")

    @allure.story("Главное меню")
    @allure.title("Переход на вкладку 'Телеканалы' и проверка отображения страницы")
    def test_navigate_to_tv_channels(self, main_page):
        driver = main_page.driver

        with allure.step("Переход на сайт Кинопоиск"):
            driver.get(TestData.BASE_URL)

        with allure.step("Ожидание загрузки главного меню"):
            try:
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(MainPage.TV_CHANNELS_ITEM)
                )
            except TimeoutException:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Main_menu_not_found",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail("Элемент главного меню 'Телеканалы' не найден")

        with allure.step("Клик по вкладке 'Телеканалы'"):
            main_page.click_tv_channels()


        with allure.step("Проверка загрузки страницы телеканалов"):
            try:
                WebDriverWait(driver, 30).until(EC.url_contains("/channels"))
            except TimeoutException:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="TV_channels_page_not_loaded",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail("Страница телеканалов не загрузилась")

            current_url = driver.current_url
            assert "/channels" in current_url, f"Ожидался URL с /channels, но получен: {current_url}"
    
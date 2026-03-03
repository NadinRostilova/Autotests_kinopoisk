import pytest
import allure
from config.test_data import TestData

@allure.feature("API Тесты Кинопоиска")
class TestKinopoiskAPI:

    @allure.story("API Кинопоиска")
    @allure.title("Получение деталей конкретного фильма по ID")
    def test_get_film_details_by_id(self, api_client):
        with allure.step("Запрашиваем детали фильма с ID 301"):
            film_data = api_client.get_film_details_by_id(TestData.MOVIE_ID)

        with allure.step("Проверяем структуру ответа"):
            assert film_data is not None
            assert "kinopoiskId" in film_data
            assert "nameRu" in film_data
            assert "ratingKinopoisk" in film_data
            assert film_data["kinopoiskId"] == TestData.MOVIE_ID


    @allure.story("API Кинопоиска")
    @allure.title("Получение списка кинопремьер")
    def test_get_premieres_list(self, api_client):
        current_year = 2025

        with allure.step(f"Запрашиваем список премьер на {current_year} год, месяц"):
            premieres = api_client.get_premieres_list(year=current_year, month="JANUARY")

        with allure.step("Проверяем структуру ответа"):
            assert "total" in premieres
            assert "items" in premieres
            assert isinstance(premieres["total"], int)
            assert isinstance(premieres["items"], list)

        if premieres["total"] > 0:
            with allure.step("Проверяем поля первой премьеры"):
                first_premiere = premieres["items"][0]
                assert "kinopoiskId" in first_premiere
                assert "nameRu" in first_premiere
                assert "year" in first_premiere
                assert "posterUrl" in first_premiere

    @allure.story("API Кинопоиска")
    @allure.title("Получение списка похожих фильмов")
    def test_get_similar_films(self, api_client):
        with allure.step("Запрашиваем похожие фильмы для фильма с ID 301"):
            similar_films = api_client.get_similar_films(TestData.MOVIE_ID)

        with allure.step("Проверяем структуру ответа"):
            assert "total" in similar_films
            assert "items" in similar_films
            assert isinstance(similar_films["total"], int)
            assert isinstance(similar_films["items"], list)

        if similar_films["total"] > 0:
            with allure.step("Проверяем поля первого похожего фильма"):
                first_film = similar_films["items"][0]
                assert "filmId" in first_film
                assert "nameRu" in first_film
                assert "posterUrl" in first_film
                assert first_film["relationType"] == "SIMILAR"

    @allure.story("API Кинопоиска")
    @allure.title("Получение фильмов по фильтрам")
    def test_get_films_by_filters(self, api_client):
        filters = {
            "genre": "драма",
            "year": "2023",
            "ratingFrom": "7",
            "order": "RATING"
        }

        with allure.step(f"Запрашиваем фильмы с фильтрами: {filters}"):
            filtered_films = api_client.get_films_by_filters(**filters)

        with allure.step("Проверяем отфильтрованные фильмы"):
            assert filtered_films is not None
            assert "items" in filtered_films
            assert len(filtered_films["items"]) > 0

            for film in filtered_films["items"]:
                if "ratingKinopoisk" in film:
                    assert film["ratingKinopoisk"] >= 7.0

    @allure.story("API Кинопоиска")
    @allure.title("Получение данных о сезонах для сериала")
    def test_get_seasons_data(self, api_client):
        with allure.step(f"Запрашиваем данные о сезонах для сериала с ID {TestData.SERIES_ID}"):
            seasons_data = api_client.get_seasons_data(TestData.SERIES_ID)

        with allure.step("Проверяем данные о сезонах"):
            assert seasons_data is not None
            assert "items" in seasons_data

            if not seasons_data["items"]:
                allure.attach("Нет данных о сезонах", name="Предупреждение")
                return

            for season in seasons_data["items"]:
                assert "number" in season
                assert "episodes" in season
                if season["episodes"]:
                    for episode in season["episodes"]:
                        assert "episodeNumber" in episode
                else:
                    allure.attach(
                "Сезон без эпизодов",
                name=f"Сезон {season['number']}"
            )    
from network_manager import NetworkManager
import pytest
from unittest.mock import patch
import requests
import allure

MOCK_HEROES_DATA = [
    {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  2, "appearance": {"gender": "male",     "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}},
    {"id":  3, "appearance": {"gender": "female",   "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  4, "appearance": {"gender": "female",   "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}},
    {"id":  5, "appearance": {"gender": "-",        "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  6, "appearance": {"gender": "-",        "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}},
    {"id":  7,                                                                      "work": {"occupation": "true",  "base": "true"}},
    {"id":  8, "appearance": {"gender": "-",        "height": ["-", "1 meters"]}},
    {"id":  9, "appearance": {"gender": "-",        "height": []}},
    {"id": 10, "appearance": {"gender": "-",        "height": ["-", "1 kg"]},       "work": {"occupation": "true",  "base": "true"}},
    ]

MOCK_EMPTY_HEROES_DATA = []

MOCK_SAME_HEROES_DATA = [
    {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  2, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  3, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    ]

MOCK_ONE_ELEMENT_HEROES_DATA = [
    {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    ]

MOCK_FILTERED_HEROES_DATA = [
    {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  2, "appearance": {"gender": "male",     "height": ["-", "1 meters"]},   "work": {"occupation": "-",     "base": "-"}},
    {"id":  3, "appearance": {"gender": "male",     "height": ["-"]},               "work": {"occupation": "-",     "base": "-"}},
    {"id":  4, "appearance": {"gender": "male",     "height": ["-", "99 kg"]},      "work": {"occupation": "-",     "base": "-"}},
    {"id":  5,                                                                      "work": {"occupation": "-",     "base": "-"}},
    {"id":  6, "appearance": {"gender": "male",     "height": []},                  "work": {"occupation": "-",     "base": "-"}},
]

class TestNetworkManager:

    @pytest.fixture
    def network_manager(self):
        return NetworkManager("https://example.com")
    
    @allure.story("Тест функции get_the_tallest_hero с моками")
    @pytest.mark.parametrize(
    "gender, has_work, expected_hero_id, heroes_data",
    [
        ("male",                False,  1,      MOCK_HEROES_DATA),  
        ("male",                True,   2,      MOCK_HEROES_DATA),
        ("female",              False,  3,      MOCK_HEROES_DATA),
        ("female",              True,   4,      MOCK_HEROES_DATA),
        ("-",                   False,  5,      MOCK_HEROES_DATA),
        ("-",                   True,   6,      MOCK_HEROES_DATA),
        ("nonexistent_gender",  False,  None,   MOCK_HEROES_DATA),
        ("nonexistent_gender",  True,   None,   MOCK_HEROES_DATA),
        ("male",                False,  None,   MOCK_EMPTY_HEROES_DATA),  
        ("male",                False,  1,      MOCK_SAME_HEROES_DATA),  
        ("male",                False,  1,      MOCK_ONE_ELEMENT_HEROES_DATA),  
    ])   
    def test_get_the_tallest_hero_with_mock(self, network_manager, gender, has_work, expected_hero_id, heroes_data):
        with allure.step("Мокаем запрос к серверу"):
            with patch("requests.get") as mock_get:
                mock_response = mock_get.return_value
                mock_response.status_code = 200
                mock_response.json.return_value = heroes_data
                with allure.step(f"Пол: {gender}, работа: {has_work}, ожидаемый id: {expected_hero_id}"):
                    result = network_manager.get_the_tallest_hero(gender, has_work)
                    if expected_hero_id is None:
                        with allure.step(f"Результат: {result}"):
                            assert result is None
                    else:
                        with allure.step(f"Результат: {result["id"]}"):
                            assert result["id"] == expected_hero_id
                            

    @allure.story("Тест функции filter_heroes с моками")
    @pytest.mark.parametrize(
    "gender, has_work, expected_result",
    [
        ("male",                False,  [{"id":  1, "appearance": {"gender": "male",    "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}}]),  
        ("male",                True,   [{"id":  2, "appearance": {"gender": "male",    "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}}]),
        ("female",              False,  [{"id":  3, "appearance": {"gender": "female",  "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}}]),
        ("female",              True,   [{"id":  4, "appearance": {"gender": "female",  "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}}]),
        ("-",                   False,  [{"id":  5, "appearance": {"gender": "-",       "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}}]),
        ("-",                   True,   [{"id":  6, "appearance": {"gender": "-",       "height": ["-", "1 meters"]},   "work": {"occupation": "true",  "base": "true"}},
                                         {"id": 10, "appearance": {"gender": "-",       "height": ["-", "1 kg"]},       "work": {"occupation": "true",  "base": "true"}}]),
        ("nonexistent_gender",  False,  []),
        ("nonexistent_gender",  True,   []),
    ])   
    def test_filter_heroes_with_mock(self, network_manager, gender, has_work, expected_result):
        with allure.step(f"Пол: {gender}, работа: {has_work}, ожидаемый id: {expected_result}"):
            result = network_manager.filter_heroes(MOCK_HEROES_DATA, gender, has_work)
            with allure.step(f"Результат: {result}"):
                assert result == expected_result


    @allure.story("Тест функции find_max с моками")
    @pytest.mark.parametrize(
    "heroes_data, expected_result",
    [
        (MOCK_FILTERED_HEROES_DATA,     {"id":  2, "appearance": {"gender": "male",     "height": ["-", "1 meters"]},   "work": {"occupation": "-",     "base": "-"}}),
        (MOCK_SAME_HEROES_DATA,         {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}}),
        (MOCK_ONE_ELEMENT_HEROES_DATA,  {"id":  1, "appearance": {"gender": "male",     "height": ["-", "99 cm"]},      "work": {"occupation": "-",     "base": "-"}}),
        (MOCK_EMPTY_HEROES_DATA,        None),
    ])   
    def test_find_max_with_mock(self, network_manager, heroes_data, expected_result):
        result = network_manager.find_max(heroes_data) 
        with allure.step(f"Результат: {result}"):
            assert result == expected_result


    @allure.story("Тест функции get_request с моками, успешный запрос")
    def test_get_request_success_with_mock(self, network_manager):
        with allure.step("Мокаем успешный запрос"):
            mock_data = {"key": "value"}
            with patch("requests.get") as mock_get:
                mock_response = mock_get.return_value
                mock_response.status_code = 200
                mock_response.json.return_value = mock_data
                result = network_manager.get_request()
                assert result == mock_data

    @allure.story("Тест функции get_request с моками, ошибка сервера")
    def test_get_request_server_error_with_mock(self, network_manager):
        with allure.step("Мокаем ошибку сервера"):
            with patch("requests.get") as mock_get:
                mock_response = mock_get.return_value
                mock_response.status_code = 500
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
                result = network_manager.get_request()
                assert result is None

    @allure.story("Тест функции get_request с моками, ошибка соединения")
    def test_get_request_connection_error_with_mock(self, network_manager):
        with allure.step("Мокаем ошибку соединения"):
            with patch("requests.get") as mock_get:
                mock_get.side_effect = requests.exceptions.ConnectionError
                result = network_manager.get_request()
                assert result is None

    @allure.story("Тест функции get_request с моками, не JSON в ответе")
    def test_get_request_invalid_json_with_mock(self, network_manager):
        with allure.step("Мокаем некорректный JSON"):
            with patch("requests.get") as mock_get:
                mock_response = mock_get.return_value
                mock_response.status_code = 200
                mock_response.json.side_effect = ValueError("Invalid JSON")
                result = network_manager.get_request()
                assert result is None


    

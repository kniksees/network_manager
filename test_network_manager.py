from network_manager import NetworkManager
import pytest
from unittest.mock import patch
import requests

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
        return NetworkManager()
    
    @pytest.mark.parametrize(
    "gender, has_work, expected_hero_id",
    [
        ("male",                False,  1),  
        ("male",                True,   2),
        ("female",              False,  3),
        ("female",              True,   4),
        ("-",                   False,  5),
        ("-",                   True,   6),
        ("nonexistent_gender",  False,  None),
        ("nonexistent_gender",  True,   None),
    ])   
    def test_get_the_tallest_hero(self, network_manager, gender, has_work, expected_hero_id):
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = MOCK_HEROES_DATA

            result = network_manager.get_the_tallest_hero(gender, has_work)
            if expected_hero_id is None:
                assert result is None
            else:
                assert result["id"] == expected_hero_id

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
    def test_filter_heroes(self, network_manager, gender, has_work, expected_result):
        assert network_manager.filter_heroes(MOCK_HEROES_DATA, gender, has_work) == expected_result


    @pytest.mark.parametrize(
    "heroes_data, expected_result",
    [
        (MOCK_FILTERED_HEROES_DATA, {"id": 2, "appearance": {"gender": "male", "height": ["-", "1 meters"]}, "work": {"occupation": "-",  "base": "-"}}),
        ([], None),
    ])   
    def test_find_max(self, network_manager, heroes_data, expected_result):
        assert network_manager.find_max(heroes_data) == expected_result



    def test_get_request_success(self, network_manager):
        url = "https://example.com"
        mock_data = {"key": "value"}
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = mock_data
            result = network_manager.get_request(url)
            assert result == mock_data

    def test_get_request_server_error(self, network_manager):
        url = "https://example.com"
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
            result = network_manager.get_request(url)
            assert result is None

    def test_get_request_connection_error(self, network_manager):
        url = "https://example.com"
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError
            result = network_manager.get_request(url)
            assert result is None

    def test_get_request_invalid_json(self, network_manager):
        url = "https://example.com"
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            result = network_manager.get_request(url)
            assert result is None


    

import pytest
import requests
from data import URL_ORDER


class TestOrderApi:

    @pytest.mark.parametrize("color", [
        [],
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"]
    ])
    def test_create_order_colors(self, requests_mock, color):
        requests_mock.post(
            URL_ORDER,
            status_code=201,
            json={"track": 111111}
        )

        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Street, 123",
            "metroStation": 4,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2025-04-12",
            "comment": "Test comment",
            "color": color
        }

        response = requests.post(URL_ORDER, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()


    def test_get_orders_list(self, requests_mock):
        requests_mock.get(
            URL_ORDER,
            status_code=200,
            json={"orders": [{"id": 1}, {"id": 2}]}
        )

        response = requests.get(URL_ORDER)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
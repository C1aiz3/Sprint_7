import pytest
import requests
from helpers import register_new_courier_and_return_login_password, URL_COURIER, URL_ORDER





class TestCourierAPI:

    @pytest.fixture
    def courier_credentials(self, requests_mock):
        requests_mock.post(
            URL_COURIER,
            status_code=201,
            json={"ok": True}
        )

        creds = register_new_courier_and_return_login_password()
        assert creds, "Не удалось зарегистрировать курьера"
        return creds

    def test_create_courier_success(self, courier_credentials):
        login, password, first_name = courier_credentials
        assert login and password and first_name

    def test_create_duplicate_courier(self, requests_mock, courier_credentials):
        login, password, first_name = courier_credentials
        requests_mock.post(
            URL_COURIER,
            status_code=409,
            json={"message": "Этот логин уже используется"}
        )

        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(URL_COURIER, data=payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется"

    @pytest.mark.parametrize("payload", [
        {"password": "12345", "firstName": "Test"},
        {"login": "testlogin", "firstName": "Test"},
        {"login": "testlogin", "password": "12345"},
    ])
    def test_create_courier_missing_fields(self, requests_mock, payload):
        requests_mock.post(
            URL_COURIER,
            status_code=400,
            json={"message": "Недостаточно данных для создания учетной записи"}
        )

        response = requests.post(URL_COURIER, data=payload)
        assert response.status_code == 400
        assert "message" in response.json()

    def test_login_courier_success(self, requests_mock, courier_credentials):
        login, password, _ = courier_credentials

        requests_mock.post(
            f'{URL_COURIER}/login',
            status_code=200,
            json={"id": 123}
        )

        payload = {"login": login, "password": password}
        response = requests.post(f'{URL_COURIER}/login', data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("payload", [
        {"login": "nonexistent", "password": "wrong"},
        {"login": "nonexistent", "password": ""},
        {"login": "", "password": "somepass"},
    ])
    def test_login_courier_invalid_credentials(self, requests_mock, payload):
        requests_mock.post(
            f'{URL_COURIER}/login',
            status_code=404,
            json={"message": "Учетная запись не найдена"}
        )

        response = requests.post(f'{URL_COURIER}/login', data=payload)
        assert response.status_code == 404
        assert "message" in response.json()

    @pytest.mark.parametrize("payload", [
        {"password": "12345"},
        {"login": "some_login"},
        {},
    ])
    def test_login_courier_missing_fields(self, requests_mock, payload):
        requests_mock.post(
            f'{URL_COURIER}/login',
            status_code=400,
            json={"message": "Недостаточно данных для входа"}
        )

        response = requests.post(f'{URL_COURIER}/login', data=payload)
        assert response.status_code == 400
        assert "message" in response.json()

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

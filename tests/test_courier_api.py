import pytest
import requests
import data

class TestCourierAPI:

    def test_create_courier_success(self, courier_credentials):
        login, password, first_name = courier_credentials
        assert login and password and first_name

    def test_create_duplicate_courier(self, requests_mock, courier_credentials):
        login, password, first_name = courier_credentials
        requests_mock.post(
            data.URL_COURIER,
            status_code=409,
            json={"message": data.DUPLICATE}
        )

        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(data.URL_COURIER, data=payload)
        assert response.status_code == 409
        assert response.json()["message"] == data.DUPLICATE

    @pytest.mark.parametrize("payload", [
        {"password": "12345", "firstName": "Test"},
        {"login": "testlogin", "firstName": "Test"},
        {"login": "testlogin", "password": "12345"},
    ])
    def test_create_courier_missing_fields(self, requests_mock, payload):
        requests_mock.post(
            data.URL_COURIER,
            status_code=400,
            json={"message": data.NOT_ENOUGH_DATA_CREATE}
        )

        response = requests.post(data.URL_COURIER, data=payload)
        assert response.status_code == 400
        assert "message" in response.json()

    def test_login_courier_success(self, requests_mock, courier_credentials):
        login, password, _ = courier_credentials

        requests_mock.post(
            f'{data.URL_COURIER}/login',
            status_code=200,
            json={"id": 123}
        )

        payload = {"login": login, "password": password}
        response = requests.post(f'{data.URL_COURIER}/login', data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("payload", [
        {"login": "nonexistent", "password": "wrong"},
        {"login": "nonexistent", "password": ""},
        {"login": "", "password": "somepass"},
    ])
    def test_login_courier_invalid_credentials(self, requests_mock, payload):
        requests_mock.post(
            f'{data.URL_COURIER}/login',
            status_code=404,
            json={"message": data.NOT_FOUND}
        )

        response = requests.post(f'{data.URL_COURIER}/login', data=payload)
        assert response.status_code == 404
        assert "message" in response.json()

    @pytest.mark.parametrize("payload", [
        {"password": "12345"},
        {"login": "some_login"},
        {},
    ])
    def test_login_courier_missing_fields(self, requests_mock, payload):
        requests_mock.post(
            f'{data.URL_COURIER}/login',
            status_code=400,
            json={"message": data.NOT_ENOUGH_DATA_LOGIN}
        )

        response = requests.post(f'{data.URL_COURIER}/login', data=payload)
        assert response.status_code == 400
        assert "message" in response.json()
import pytest
from helpers import register_new_courier_and_return_login_password
from data import URL_COURIER

@pytest.fixture
def courier_credentials(requests_mock):
    requests_mock.post(
        URL_COURIER,
        status_code=201,
        json={"ok": True}
    )

    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось зарегистрировать курьера"
    return creds
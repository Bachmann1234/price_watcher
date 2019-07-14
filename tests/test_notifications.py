from unittest.mock import Mock, call
from price_watcher import notifications
from price_watcher.notifications import SID_ENV, AUTH_ENV, PHONE_NUM_ENV, send_text


def test_send_text(monkeypatch):
    monkeypatch.setenv(SID_ENV, "sid")
    monkeypatch.setenv(AUTH_ENV, "auth")
    monkeypatch.setenv(PHONE_NUM_ENV, "phone")
    test_client = Mock()
    monkeypatch.setattr(notifications, "TwilioClient", test_client)
    send_text("Test", "2025550112")
    assert test_client.mock_calls == [
        call("sid", "auth"),
        call().messages.create(body="Test", from_="phone", to="2025550112"),
    ]

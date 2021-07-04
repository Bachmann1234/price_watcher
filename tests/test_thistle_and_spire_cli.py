from unittest.mock import Mock, call

from click.testing import CliRunner

from price_watcher import cli
from price_watcher.cli import check_thistle_and_spire_cli


def _set_mocks(monkeypatch):
    send_text = Mock()
    monkeypatch.setattr(cli, "get_product_status", lambda _: {"S": True, "XL": False})
    monkeypatch.setattr(cli, "send_text", send_text)
    return send_text


def test_check_product_in_stock(monkeypatch):
    send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(
        check_thistle_and_spire_cli, ["medusa-bralette-chameleon", "S", "2025550112"]
    )
    assert result.exit_code == 0
    assert result.output == "medusa-bralette-chameleon in size S is in stock!\n"
    assert send_text.mock_calls == [
        call("medusa-bralette-chameleon in size S is in stock!", "2025550112")
    ]


def test_check_product_out_of_stock(monkeypatch):
    send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(
        check_thistle_and_spire_cli, ["medusa-bralette-chameleon", "XL", "2025550112"]
    )
    assert result.exit_code == 0
    assert result.output == "medusa-bralette-chameleon in size XL is not in stock!\n"
    send_text.assert_not_called()

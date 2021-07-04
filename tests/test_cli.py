from unittest.mock import Mock, call

from click.testing import CliRunner

from price_watcher import cli
from price_watcher.amazon import ProductInfo
from price_watcher.cli import check_amazon_cli


def _set_mocks(monkeypatch):
    product_info = Mock(
        return_value=ProductInfo(name="Cool Product", prices=[100, 200])
    )
    get_url = Mock(return_value="https://www.example.com")
    send_text = Mock()
    monkeypatch.setattr(cli, "get_product_info", product_info)
    monkeypatch.setattr(cli, "get_url", get_url)
    monkeypatch.setattr(cli, "send_text", send_text)
    return product_info, get_url, send_text


def test_check_product_cli_below_target(monkeypatch):
    _, _, send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(check_amazon_cli, ["123", "1000", "2025550112"])
    assert result.exit_code == 0
    assert result.output == "ProductInfo(name='Cool Product', prices=[100, 200])\n"
    assert send_text.mock_calls == [
        call("Found Cool Product for $100! https://www.example.com", "2025550112")
    ]


def test_check_product_cli_below_above_target(monkeypatch):
    _, _, send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(check_amazon_cli, ["123", "10", "2025550112"])
    assert result.exit_code == 0
    assert result.output == "ProductInfo(name='Cool Product', prices=[100, 200])\n"
    send_text.assert_not_called()

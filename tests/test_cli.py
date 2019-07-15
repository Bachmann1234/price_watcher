from datetime import datetime
from unittest.mock import Mock, call

from click.testing import CliRunner

from price_watcher import cli
from price_watcher.amazon import ProductInfo
from price_watcher.cli import check_product


class MockDatetime(object):
    @classmethod
    def utcnow(cls):
        return datetime.utcfromtimestamp(1563137468.201281)


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


def test_check_product_below_target(monkeypatch):
    _, _, send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(check_product, ["123", "1000", "2025550112"])
    assert result.exit_code == 0
    assert result.output == "ProductInfo(name='Cool Product', prices=[100, 200])\n"
    assert send_text.mock_calls == [
        call("Found Cool Product for $100! https://www.example.com", "2025550112")
    ]


def test_check_product_below_above_target(monkeypatch):
    _, _, send_text = _set_mocks(monkeypatch)
    runner = CliRunner()
    result = runner.invoke(check_product, ["123", "10", "2025550112"])
    assert result.exit_code == 0
    assert result.output == "ProductInfo(name='Cool Product', prices=[100, 200])\n"
    send_text.assert_not_called()


def test_check_product_below_history_file(monkeypatch, tmp_path):
    _set_mocks(monkeypatch)
    monkeypatch.setattr(cli, "datetime", MockDatetime)
    history_file = tmp_path / "cool.txt"
    runner = CliRunner()
    runner.invoke(
        check_product, ["123", "10", "2025550112", "--history_file", str(history_file)]
    )
    monkeypatch.setattr(
        cli,
        "get_product_info",
        Mock(return_value=ProductInfo(name="Cool Product", prices=[900, 800])),
    )
    runner.invoke(
        check_product, ["123", "10", "2025550112", "--history_file", str(history_file)]
    )
    with open(history_file, "r") as infile:
        result = infile.read()
        assert (
            "2019-07-14T20:51:08.201281|100,200\n2019-07-14T20:51:08.201281|900,800\n"
            == result
        )

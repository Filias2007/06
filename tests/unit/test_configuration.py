"""Unit tests for configuration via environment variables."""

from __future__ import annotations

from shop.services import get_min_stock, get_payment_mode


def test_payment_mode_from_env(monkeypatch) -> None:
    monkeypatch.setenv("PAYMENT_MODE", "test")
    assert get_payment_mode() == "test"


def test_default_payment_mode(monkeypatch) -> None:
    monkeypatch.delenv("PAYMENT_MODE", raising=False)
    assert get_payment_mode() == "sandbox"


def test_min_stock_from_env(monkeypatch) -> None:
    monkeypatch.setenv("MIN_STOCK", "10")
    assert get_min_stock() == 10


def test_default_min_stock(monkeypatch) -> None:
    monkeypatch.delenv("MIN_STOCK", raising=False)
    assert get_min_stock() == 5

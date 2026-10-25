"""Unit tests for Money value object."""

from __future__ import annotations

import pytest

from shop.value_objects import Money


def test_money_creation() -> None:
    money = Money(100, "UAH")
    assert money.amount == 100
    assert money.currency == "UAH"


def test_negative_money_rejected() -> None:
    with pytest.raises(ValueError, match="negative"):
        Money(-1, "UAH")


def test_money_addition() -> None:
    result = Money(100) + Money(50)
    assert result == Money(150)


def test_currency_mismatch() -> None:
    with pytest.raises(ValueError, match="Currency"):
        Money(100, "UAH") + Money(10, "USD")


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (0, 0),
        (0.01, 0.01),
        (100, 100),
        (9999.99, 9999.99),
    ],
)
def test_valid_money_amounts(amount: float, expected: float) -> None:
    money = Money(amount)
    assert money.amount == pytest.approx(expected)


def test_money_multiplication() -> None:
    result = Money(50) * 3
    assert result.amount == pytest.approx(150)

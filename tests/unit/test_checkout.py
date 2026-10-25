"""Unit tests for CheckoutService with Mock."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from shop.models import Cart
from shop.protocols import Notifier, PaymentGateway
from shop.services import CheckoutService, PaymentError


def test_checkout_success(cart) -> None:
    gateway = Mock(spec=PaymentGateway)
    gateway.pay.return_value = "PAY-001"
    notifier = Mock(spec=Notifier)

    service = CheckoutService(payment_gateway=gateway, notifier=notifier)
    result = service.checkout("anna@example.com", cart)

    assert result == "PAY-001"
    gateway.pay.assert_called_once_with(cart.total)
    notifier.send.assert_called_once_with(
        "anna@example.com",
        "Payment successful: PAY-001",
    )


def test_checkout_payment_failure(cart) -> None:
    gateway = Mock(spec=PaymentGateway)
    gateway.pay.side_effect = PaymentError("Unavailable")
    notifier = Mock(spec=Notifier)

    service = CheckoutService(gateway, notifier)

    with pytest.raises(PaymentError, match="Unavailable"):
        service.checkout("anna@example.com", cart)

    notifier.send.assert_not_called()


def test_empty_cart_checkout() -> None:
    gateway = Mock(spec=PaymentGateway)
    notifier = Mock(spec=Notifier)
    service = CheckoutService(gateway, notifier)

    with pytest.raises(ValueError, match="empty"):
        service.checkout("anna@example.com", Cart())

    gateway.pay.assert_not_called()
    notifier.send.assert_not_called()

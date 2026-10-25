"""Business services: discount, checkout, config, async price."""

from __future__ import annotations

import os

from shop.models import Cart
from shop.protocols import AsyncPriceProvider, Notifier, PaymentGateway
from shop.value_objects import Money


class PaymentError(Exception):
    """Payment gateway failure."""


class PercentageDiscount:
    def __init__(self, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("Invalid discount")
        self.percent = percent

    def apply(self, total: Money) -> Money:
        return Money(
            total.amount * (1 - self.percent / 100),
            total.currency,
        )


class CheckoutService:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        notifier: Notifier,
    ) -> None:
        self._gateway = payment_gateway
        self._notifier = notifier

    def checkout(self, email: str, cart: Cart) -> str:
        if len(cart) == 0:
            raise ValueError("Cart is empty")
        payment_id = self._gateway.pay(cart.total)
        self._notifier.send(
            email,
            f"Payment successful: {payment_id}",
        )
        return payment_id


def get_payment_mode() -> str:
    return os.getenv("PAYMENT_MODE", "sandbox")


def get_min_stock() -> int:
    raw = os.getenv("MIN_STOCK", "5")
    return int(raw)


class AsyncPriceService:
    def __init__(self, provider: AsyncPriceProvider) -> None:
        self._provider = provider

    async def get_price(self, product_id: int) -> float:
        return await self._provider.fetch_price(product_id)

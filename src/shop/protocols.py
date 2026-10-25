"""Protocols (interfaces) for external dependencies."""

from __future__ import annotations

from typing import Protocol

from shop.models import Product
from shop.value_objects import Money


class PaymentGateway(Protocol):
    def pay(self, amount: Money) -> str: ...


class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None: ...


class ProductRepository(Protocol):
    def get(self, product_id: int) -> Product | None: ...
    def save(self, product: Product) -> None: ...
    def list_all(self) -> list[Product]: ...


class AsyncPriceProvider(Protocol):
    async def fetch_price(self, product_id: int) -> float: ...

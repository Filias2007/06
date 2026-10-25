"""Shared fixtures for the online store test suite."""

from __future__ import annotations

import pytest

from shop.models import Cart, Product
from shop.value_objects import Money


@pytest.fixture
def laptop() -> Product:
    return Product(
        product_id=1,
        name="Laptop",
        category="Electronics",
        price=Money(35_000),
        quantity=10,
    )


@pytest.fixture
def mouse() -> Product:
    return Product(
        product_id=2,
        name="Mouse",
        category="Electronics",
        price=Money(1_200),
        quantity=50,
    )


@pytest.fixture
def book() -> Product:
    return Product(
        product_id=3,
        name="Python Book",
        category="Books",
        price=Money(450),
        quantity=20,
    )


@pytest.fixture
def cart(laptop: Product, mouse: Product) -> Cart:
    c = Cart()
    c.add(laptop, 1)
    c.add(mouse, 2)
    return c


@pytest.fixture
def product_factory():
    """Factory fixture for creating products with custom fields."""

    def create(
        *,
        product_id: int = 1,
        name: str = "Product",
        category: str = "General",
        price: float = 100.0,
        quantity: int = 1,
    ) -> Product:
        return Product(
            product_id=product_id,
            name=name,
            category=category,
            price=Money(price),
            quantity=quantity,
        )

    return create

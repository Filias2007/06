"""Unit tests for Product, Cart, Catalog."""

from __future__ import annotations

import pytest

from shop.models import Cart, Catalog, Product, ProductValidationError
from shop.value_objects import Money


def test_product_creation(laptop: Product) -> None:
    assert laptop.name == "Laptop"
    assert laptop.category == "Electronics"
    assert laptop.price.amount == pytest.approx(35_000)
    assert laptop.quantity == 10


def test_empty_name_rejected() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product(
            product_id=1,
            name="  ",
            category="X",
            price=Money(10),
            quantity=1,
        )
    assert exc_info.value.field == "name"


def test_negative_quantity_rejected() -> None:
    with pytest.raises(ProductValidationError) as exc_info:
        Product(
            product_id=1,
            name="Item",
            category="X",
            price=Money(10),
            quantity=-1,
        )
    assert exc_info.value.field == "quantity"


def test_empty_cart() -> None:
    cart = Cart()
    assert len(cart) == 0
    assert cart.total.amount == 0


def test_cart_length(cart: Cart) -> None:
    assert len(cart) == 2


def test_cart_contains_product(cart: Cart) -> None:
    assert 1 in cart
    assert 2 in cart
    assert 999 not in cart


def test_cart_total(cart: Cart) -> None:
    # 35000 + 2*1200 = 37400
    assert cart.total.amount == pytest.approx(37_400)


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_invalid_quantity(laptop: Product, quantity: int) -> None:
    cart = Cart()
    with pytest.raises(ValueError, match="positive"):
        cart.add(laptop, quantity)


def test_catalog_add_and_find(product_factory) -> None:
    catalog = Catalog()
    p = product_factory(product_id=10, name="Phone", price=5000)
    catalog.add(p)
    found = catalog.find_by_id(10)
    assert found is not None
    assert found.name == "Phone"
    assert catalog.find_by_id(999) is None


def test_catalog_filter_by_category(laptop: Product, mouse: Product, book: Product) -> None:
    catalog = Catalog()
    catalog.add(laptop)
    catalog.add(mouse)
    catalog.add(book)
    electronics = catalog.filter_by_category("Electronics")
    assert len(electronics) == 2
    assert all(p.category == "Electronics" for p in electronics)


def test_catalog_stock_value(laptop: Product, mouse: Product) -> None:
    catalog = Catalog()
    catalog.add(laptop)
    catalog.add(mouse)
    # 35000*10 + 1200*50 = 350000 + 60000 = 410000
    assert catalog.stock_value() == pytest.approx(410_000)


def test_catalog_most_expensive(laptop: Product, mouse: Product, book: Product) -> None:
    catalog = Catalog()
    catalog.add(laptop)
    catalog.add(mouse)
    catalog.add(book)
    top = catalog.most_expensive()
    assert top is not None
    assert top.name == "Laptop"


def test_empty_catalog() -> None:
    catalog = Catalog()
    assert catalog.stock_value() == 0
    assert catalog.most_expensive() is None
    assert catalog.filter_by_category("Any") == []

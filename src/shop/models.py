"""Domain models: Product, Cart, Catalog."""

from __future__ import annotations

from dataclasses import dataclass, field

from shop.value_objects import Money


class ProductValidationError(Exception):
    """Raised when product data is invalid."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")


@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    category: str
    price: Money
    quantity: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ProductValidationError("name", "must not be empty")
        if self.price.amount < 0:
            raise ProductValidationError("price", "must be non-negative")
        if self.quantity < 0:
            raise ProductValidationError("quantity", "must be non-negative")


@dataclass
class CartItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def total(self) -> Money:
        return Money(
            self.product.price.amount * self.quantity,
            self.product.price.currency,
        )


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1) -> None:
        self.items.append(CartItem(product, quantity))

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, product_id: int) -> bool:
        return any(item.product.product_id == product_id for item in self.items)

    @property
    def total(self) -> Money:
        if not self.items:
            return Money(0)
        return Money(sum(item.total.amount for item in self.items))


@dataclass
class Catalog:
    """In-memory product catalog."""

    products: list[Product] = field(default_factory=list)

    def add(self, product: Product) -> None:
        self.products.append(product)

    def find_by_id(self, product_id: int) -> Product | None:
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def filter_by_category(self, category: str) -> list[Product]:
        return [p for p in self.products if p.category == category]

    def stock_value(self) -> float:
        return sum(p.price.amount * p.quantity for p in self.products)

    def most_expensive(self) -> Product | None:
        if not self.products:
            return None
        return max(self.products, key=lambda p: p.price.amount)

"""Import/export helpers (CSV, JSON)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from shop.models import Product, ProductValidationError
from shop.value_objects import Money


class DataImportError(Exception):
    """Raised when CSV/JSON import fails."""


def export_order(order: dict, path: Path) -> None:
    path.write_text(
        json.dumps(order, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def import_products_csv(path: Path) -> list[Product]:
    """Import products from CSV: id,name,category,price,quantity."""
    products: list[Product] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                product = Product(
                    product_id=int(row["id"]),
                    name=row["name"],
                    category=row["category"],
                    price=Money(float(row["price"])),
                    quantity=int(row["quantity"]),
                )
            except (KeyError, ValueError, ProductValidationError) as err:
                raise DataImportError(f"Malformed product record: {row}") from err
            products.append(product)
    return products


def export_products_json(products: list[Product], path: Path) -> None:
    data = [
        {
            "id": p.product_id,
            "name": p.name,
            "category": p.category,
            "price": p.price.amount,
            "quantity": p.quantity,
        }
        for p in products
    ]
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

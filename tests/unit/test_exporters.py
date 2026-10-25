"""Unit tests for CSV import / JSON export (tmp_path)."""

from __future__ import annotations

import json

import pytest

from shop.exporters import DataImportError, export_order, export_products_json, import_products_csv
from shop.models import Product
from shop.value_objects import Money


def test_export_order(tmp_path) -> None:
    output = tmp_path / "order.json"
    order = {"id": 1, "total": 100.0, "status": "paid"}
    export_order(order, output)
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data == order


def test_import_products_csv(tmp_path) -> None:
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "id,name,category,price,quantity\n"
        "1,Laptop,Electronics,35000,5\n"
        "2,Book,Books,200,10\n",
        encoding="utf-8",
    )
    products = import_products_csv(csv_file)
    assert len(products) == 2
    assert products[0].name == "Laptop"
    assert products[0].price.amount == pytest.approx(35000)
    assert products[1].category == "Books"


def test_malformed_csv_raises(tmp_path) -> None:
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "id,name,category,price,quantity\n"
        "1,Bad,Cat,not_a_number,5\n",
        encoding="utf-8",
    )
    with pytest.raises(DataImportError, match="Malformed"):
        import_products_csv(csv_file)


def test_export_products_json(tmp_path, laptop: Product) -> None:
    output = tmp_path / "catalog.json"
    export_products_json([laptop], output)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"
    assert data[0]["price"] == pytest.approx(35000)

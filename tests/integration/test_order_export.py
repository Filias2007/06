"""Integration tests: cart + checkout + export pipeline."""

from __future__ import annotations

import json
from unittest.mock import Mock

import pytest

from shop.exporters import export_order, export_products_json, import_products_csv
from shop.models import Catalog
from shop.protocols import Notifier, PaymentGateway
from shop.services import CheckoutService


@pytest.mark.integration
def test_order_export_integration(tmp_path, cart) -> None:
    gateway = Mock(spec=PaymentGateway)
    gateway.pay.return_value = "PAY-100"
    notifier = Mock(spec=Notifier)

    service = CheckoutService(gateway, notifier)
    payment_id = service.checkout("anna@example.com", cart)

    output = tmp_path / "order.json"
    export_order(
        {
            "payment_id": payment_id,
            "total": cart.total.amount,
        },
        output,
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["payment_id"] == "PAY-100"
    assert data["total"] == pytest.approx(37_400)
    notifier.send.assert_called_once()


@pytest.mark.integration
def test_import_process_export_pipeline(tmp_path) -> None:
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "id,name,category,price,quantity\n"
        "1,Laptop,Electronics,35000,3\n"
        "2,Mouse,Electronics,500,10\n"
        "3,Book,Books,200,5\n",
        encoding="utf-8",
    )

    products = import_products_csv(csv_file)
    catalog = Catalog()
    for p in products:
        catalog.add(p)

    assert catalog.stock_value() == pytest.approx(35000 * 3 + 500 * 10 + 200 * 5)
    electronics = catalog.filter_by_category("Electronics")
    assert len(electronics) == 2

    out = tmp_path / "catalog.json"
    export_products_json(catalog.products, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 3
    assert data[0]["name"] == "Laptop"


@pytest.mark.integration
def test_checkout_then_catalog_stock(tmp_path, product_factory) -> None:
    """Integration: products in catalog, cart, checkout, export."""
    catalog = Catalog()
    p1 = product_factory(product_id=1, name="Item A", price=100, quantity=5)
    p2 = product_factory(product_id=2, name="Item B", price=50, quantity=10)
    catalog.add(p1)
    catalog.add(p2)

    from shop.models import Cart

    cart = Cart()
    cart.add(p1, 2)
    cart.add(p2, 1)

    gateway = Mock(spec=PaymentGateway)
    gateway.pay.return_value = "PAY-200"
    notifier = Mock(spec=Notifier)
    service = CheckoutService(gateway, notifier)

    pid = service.checkout("buyer@shop.local", cart)
    assert pid == "PAY-200"

    report = tmp_path / "report.json"
    export_order(
        {
            "payment_id": pid,
            "items": len(cart),
            "total": cart.total.amount,
            "catalog_value": catalog.stock_value(),
        },
        report,
    )
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["total"] == pytest.approx(250)
    assert data["catalog_value"] == pytest.approx(1000)

# Online Store — Lab 06 (variant 3)

Automated testing suite for the Internet shop domain model.

## Run tests

```bash
python -m pip install -e ".[dev]"
pytest -v
pytest -v --cov=shop --cov-branch --cov-report=term-missing
```

## Structure

```
LAB_06/
├── src/shop/          # production code
│   ├── models.py      # Product, Cart, Catalog
│   ├── value_objects.py
│   ├── services.py    # Discount, Checkout, config, async
│   ├── exporters.py   # CSV import / JSON export
│   └── protocols.py
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

## Coverage

Target ≥ 80% (branch). Current run: ~99% statement, high branch coverage.

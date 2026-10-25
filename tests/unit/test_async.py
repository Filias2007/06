"""Async unit tests with AsyncMock."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from shop.services import AsyncPriceService


@pytest.mark.asyncio
async def test_async_price_success() -> None:
    provider = AsyncMock()
    provider.fetch_price.return_value = 99.5
    service = AsyncPriceService(provider)

    result = await service.get_price(42)

    assert result == pytest.approx(99.5)
    provider.fetch_price.assert_awaited_once_with(42)


@pytest.mark.asyncio
async def test_async_price_error() -> None:
    provider = AsyncMock()
    provider.fetch_price.side_effect = ConnectionError("Network error")
    service = AsyncPriceService(provider)

    with pytest.raises(ConnectionError, match="Network"):
        await service.get_price(1)

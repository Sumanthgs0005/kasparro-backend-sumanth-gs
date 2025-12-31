import pytest
from app.schemas.coin_raw import CoinRaw
from app.schemas.coin_normalized import CoinNormalized
from datetime import datetime

@pytest.mark.parametrize("raw_coin,expected_normalized", [
    (
        CoinRaw(id="btc", symbol="btc", name="Bitcoin", price_usd=45000.0),
        CoinNormalized(coin_id="btc", symbol="BTC", name="Bitcoin", price_usd=45000.0)
    )
])
def test_coin_normalization(raw_coin, expected_normalized):
    """Test coin raw to normalized transformation."""
    normalized = CoinNormalized.model_validate(raw_coin)
    assert normalized.coin_id == raw_coin.id
    assert normalized.symbol == raw_coin.symbol.upper()
    assert normalized.price_usd == raw_coin.price_usd

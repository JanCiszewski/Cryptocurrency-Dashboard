def test_get_all_coins_returns_200_and_list(client, monkeypatch):
    from app.services import crypto_service

    monkeypatch.setattr(
        crypto_service,
        "get_coins",
        lambda: [
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "btc",
                "price": 65000.0,
            }
        ],
    )

    response = client.get("/coins/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "bitcoin"


def test_get_single_coin_returns_required_fields(client, monkeypatch):
    from app.services import crypto_service

    monkeypatch.setattr(
        crypto_service,
        "get_coin",
        lambda coin_id: {
            "id": coin_id,
            "name": "Bitcoin",
            "symbol": "btc",
            "price": 65000.0,
        },
    )

    response = client.get("/coins/bitcoin")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "symbol" in data
    assert "name" in data
    assert "price" in data


def test_get_single_coin_wrong_id_returns_404(client, monkeypatch):
    from app.services import crypto_service

    monkeypatch.setattr(
        crypto_service,
        "get_coin",
        lambda coin_id: {"error": "Coin not found"},
    )

    response = client.get("/coins/not-existing-coin")

    assert response.status_code == 404

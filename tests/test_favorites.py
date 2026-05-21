def test_get_favorites_returns_200_and_list(client):
    response = client.get("/favorites/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_favorite_returns_200(client):
    response = client.post("/favorites/bitcoin")

    assert response.status_code == 200
    assert "Dodano bitcoin" in response.json()["message"]


def test_update_favorite_note_returns_200(client):
    response = client.put(
        "/favorites/bitcoin",
        params={"note": "moja notatka"},
    )

    assert response.status_code == 200
    assert response.json()["note"] == "moja notatka"


def test_delete_favorite_returns_200(client):
    response = client.delete("/favorites/bitcoin")

    assert response.status_code == 200
    assert "Usunięto bitcoin" in response.json()["message"]


def test_favorites_should_be_protected_by_jwt_but_currently_are_not(client):
    """
    Ten test jest kontrolny dla QA:
    według założeń projektu favorites powinno być zabezpieczone JWT.
    Obecny backend zwraca 200 bez tokena, więc technicznie endpoint działa,
    ale autoryzacja nie jest jeszcze wdrożona.
    """
    response = client.get("/favorites/")

    assert response.status_code == 200

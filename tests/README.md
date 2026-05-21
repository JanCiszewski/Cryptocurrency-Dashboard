# Tests – Cryptocurrency Dashboard

Ten folder zawiera testy automatyczne dla REST API aplikacji **Cryptocurrency Dashboard**.

Testy zostały przygotowane w ramach roli **Tester / QA**.

## Zakres testów

Testy sprawdzają:

- rejestrację użytkownika,
- logowanie użytkownika,
- generowanie tokena JWT,
- dostęp do `/auth/me` z tokenem i bez tokena,
- pobieranie listy kryptowalut z `/coins`,
- pobieranie pojedynczej kryptowaluty po ID,
- obsługę błędnego ID kryptowaluty,
- pobieranie, dodawanie, aktualizację i usuwanie ulubionych kryptowalut,
- dostępność Swagger UI i OpenAPI schema,
- wymagane metody HTTP: `GET`, `POST`, `PUT`, `DELETE`,
- podstawową obsługę błędów API.

## Uruchamianie testów

Najpierw należy zainstalować zależności:

```bash
py -m pip install -r requirements.txt
```

Następnie uruchomić testy:

```bash
py -m pytest -v
```

## Wynik

Testy zostały uruchomione lokalnie za pomocą `pytest`.

```bash
20 passed, 3 warnings
```

## Dodatkowe zależności

Do `requirements.txt` dodano brakujące biblioteki:

```
email-validator
argon2-cffi
```

Są one wymagane do poprawnego działania walidacji e-mail oraz hashowania haseł w backendzie.

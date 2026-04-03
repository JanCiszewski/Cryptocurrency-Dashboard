# Tests – Cryptocurrency Dashboard

## Auth
- rejestracja poprawna
- rejestracja bez maila lub hasła
- logowanie poprawne
- logowanie złym hasłem
- czy login zwraca token

## Coins
- GET /coins → 200
- GET /coins → zwraca listę
- GET /coins/{id} → poprawne id → 200
- GET /coins/{id} → złe id → 404

## Favorites
- bez tokena → 401
- z tokenem → 200
- dodawanie do favorites działa
- usuwanie z favorites działa

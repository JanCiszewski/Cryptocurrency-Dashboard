# Crypto API + PayU Integration

## Opis
Projekt backendowy umożliwiający:
- pobieranie kursów kryptowalut (CoinGecko API)
- tworzenie płatności (PayU sandbox)
- sprawdzanie statusu płatności

## Wymagania
- Python 3.x
- biblioteka requests

Instalacja:
pip install requests

## Funkcje

### crypto_service.py
- get_coins() → lista kryptowalut
- get_coin(id) → szczegóły jednej kryptowaluty

### payu_service.py
- create_payment(...) → tworzy płatność
- get_payment(order_id) → sprawdza status płatności

## Uwagi
- projekt używa PayU sandbox
- brak webhooków i bazy danych (część innych członków zespołu)

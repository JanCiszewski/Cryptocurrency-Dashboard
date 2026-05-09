import uuid
import requests

PAYU_AUTH_URL = "https://secure.snd.payu.com/pl/standard/user/oauth/authorize"
PAYU_ORDERS_URL = "https://secure.snd.payu.com/api/v2_1/orders"
PAYU_ORDER_URL = "https://secure.snd.payu.com/api/v2_1/orders/"

PAYU_CLIENT_ID = "300746"
PAYU_CLIENT_SECRET = "2ee86a66e5d97e3fadc400c9f19b065d"
PAYU_POS_ID = "300746"

def get_payu_token():

    data = {
        "grant_type": "client_credentials",
        "client_id": PAYU_CLIENT_ID,
        "client_secret": PAYU_CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            PAYU_AUTH_URL,
            data=data,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        token_data = response.json()

        return {
            "access_token": token_data.get("access_token"),
            "token_type": token_data.get("token_type"),
            "expires_in": token_data.get("expires_in")
        }

    except requests.exceptions.Timeout:
        return {"error": "PayU nie odpowiedziało na czas podczas pobierania tokena"}

    except requests.exceptions.RequestException as error:
        return {"error": f"Błąd pobierania tokena PayU: {error}"}


def create_payment(
    total_amount,
    description,
    buyer_email,
    continue_url,
    notify_url,
    customer_ip,
    product_name="Crypto top-up",
    currency_code="PLN",
    buyer_language="pl",
    ext_order_id=None
):
    if total_amount is None:
        return {"error": "Brak kwoty płatności"}

    try:
        total_amount = int(total_amount)
    except (TypeError, ValueError):
        return {"error": "Kwota płatności musi być liczbą całkowitą"}

    if total_amount <= 0:
        return {"error": "Kwota płatności musi być większa od 0"}

    if not description or not str(description).strip():
        return {"error": "Brak opisu płatności"}

    if not buyer_email or "@" not in buyer_email:
        return {"error": "Nieprawidłowy email kupującego"}

    if not continue_url or not str(continue_url).strip():
        return {"error": "Brak continue_url"}

    if not notify_url or not str(notify_url).strip():
        return {"error": "Brak notify_url"}

    if not customer_ip or not str(customer_ip).strip():
        return {"error": "Brak customer_ip"}

    if not product_name or not str(product_name).strip():
        return {"error": "Brak nazwy produktu"}

    if not currency_code or not str(currency_code).strip():
        return {"error": "Brak currency_code"}

    if not buyer_language or not str(buyer_language).strip():
        return {"error": "Brak buyer_language"}


    token_result = get_payu_token()

    if "error" in token_result:
        return token_result

    access_token = token_result["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "notifyUrl": notify_url,
        "customerIp": customer_ip,
        "merchantPosId": PAYU_POS_ID,
        "description": description,
        "currencyCode": currency_code,
        "totalAmount": str(total_amount),
        "continueUrl": continue_url,
        "buyer": {
            "email": buyer_email,
            "language": buyer_language
        },
        "products": [
            {
                "name": product_name,
                "unitPrice": str(total_amount),
                "quantity": "1"
            }
        ]
    }

    if ext_order_id:
        payload["extOrderId"] = ext_order_id
    else:
        payload["extOrderId"] = str(uuid.uuid4())

    try:
        response = requests.post(
            PAYU_ORDERS_URL,
            json=payload,
            headers=headers,
            timeout=10,
            allow_redirects=False
        )

        if response.status_code == 302:
            location = response.headers.get("Location")
            try:
                data = response.json()
            except ValueError:
                data = {}

            return {
                "order_id": data.get("orderId"),
                "ext_order_id": data.get("extOrderId"),
                "status": data.get("status", {}).get("statusCode", "SUCCESS"),
                "redirect_uri": data.get("redirectUri") or location
            }

        if response.status_code in [200, 201]:
            data = response.json()
            return {
                "order_id": data.get("orderId"),
                "ext_order_id": data.get("extOrderId"),
                "status": data.get("status", {}).get("statusCode"),
                "redirect_uri": data.get("redirectUri")
            }

        return {
            "error": f"PayU zwróciło status {response.status_code}",
            "details": response.text
        }

    except requests.exceptions.Timeout:
        return {"error": "PayU nie odpowiedziało na czas podczas tworzenia płatności"}

    except requests.exceptions.RequestException as error:
        return {"error": f"Błąd tworzenia płatności PayU: {error}"}


def get_payment(order_id):

    if not order_id or not str(order_id).strip():
        return {"error": "Brak order_id"}

    token_result = get_payu_token()

    if "error" in token_result:
        return token_result

    access_token = token_result["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(
            f"{PAYU_ORDER_URL}{order_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        orders = data.get("orders", [])

        if not orders:
            return {"error": "PayU nie zwróciło danych zamówienia"}

        order = orders[0]

        return {
            "order_id": order.get("orderId"),
            "ext_order_id": order.get("extOrderId"),
            "status": order.get("status"),
            "currency_code": order.get("currencyCode"),
            "total_amount": order.get("totalAmount"),
            "description": order.get("description"),
            "buyer_email": order.get("buyer", {}).get("email")
        }

    except requests.exceptions.Timeout:
        return {"error": "PayU nie odpowiedziało na czas podczas pobierania płatności"}

    except requests.exceptions.RequestException as error:
        return {"error": f"Błąd pobierania płatności PayU: {error}"}

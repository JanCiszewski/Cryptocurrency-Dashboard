def get_methods_from_openapi(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

    methods = []
    for path_data in response.json()["paths"].values():
        methods.extend(path_data.keys())

    return methods


def test_swagger_docs_available(client):
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_schema_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_api_has_get_post_put_delete_methods(client):
    methods = get_methods_from_openapi(client)

    assert "get" in methods
    assert "post" in methods
    assert "put" in methods
    assert "delete" in methods


def test_required_endpoints_exist(client):
    response = client.get("/openapi.json")
    paths = response.json()["paths"].keys()

    assert any(path.startswith("/coins") for path in paths)
    assert any(path.startswith("/auth/register") for path in paths)
    assert any(path.startswith("/auth/login") for path in paths)
    assert any(path.startswith("/favorites") for path in paths)


def test_payments_endpoint_exists_as_second_external_api_integration(client):
    response = client.get("/openapi.json")
    paths = response.json()["paths"].keys()

    assert any(path.startswith("/payments") for path in paths)

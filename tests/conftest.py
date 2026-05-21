import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture()
def client():
    from app.main import app
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_fake_users_db():
    """
    Czyścimy testową bazę użytkowników przed każdym testem,
    żeby testy nie wpływały na siebie nawzajem.
    """
    try:
        from app.routers.auth import fake_users_db
        fake_users_db.clear()
    except Exception:
        pass
    yield

import pytest
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_app_index_page(client):
    response = client.get("/")
    assert b"Web App with Python Flask" in response.data

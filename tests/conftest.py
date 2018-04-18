import pytest

from app import create_app

@pytest.fixture
async def client(test_client):
    return await test_client(create_app)

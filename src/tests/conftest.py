from aiohttp import web
import pytest
from src.app.main import make_app

@pytest.fixture
def client(loop, aiohttp_client):
    
    app = make_app()

    return loop.run_until_complete(aiohttp_client(app))
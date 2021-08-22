from aiohttp import web
import pytest
from src.app.main import setup_app

@pytest.fixture
def client(loop, aiohttp_client):
    app = web.Application()
    
    setup_app(app)

    return loop.run_until_complete(aiohttp_client(app))
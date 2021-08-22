from aiohttp import web
import json
import pytest
from src.app.main import setup_app

@pytest.fixture
def client(loop, aiohttp_client):
    app = web.Application()
    
    setup_app(app)

    return loop.run_until_complete(aiohttp_client(app))

async def test_hello(client):

    resp = await client.get('/')
    assert resp.status == 200

    expected_response = json.dumps({
        'hello': 'world!'
    })

    assert (await resp.text()) == expected_response

async def test_ping(client):

    resp = await client.get('/ping')

    assert resp.status == 200

    assert (await resp.text()) == 'pong'
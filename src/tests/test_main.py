from aiohttp import web
import json
from src.app.main import app
    
async def test_hello(aiohttp_client):
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert resp.status == 200

    expected_response = json.dumps({
        'hello': 'world!'
    })

    assert (await resp.text()) == expected_response
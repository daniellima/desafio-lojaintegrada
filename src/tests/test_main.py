async def test_hello(client):

    resp = await client.get('/')
    assert resp.status == 200

async def test_ping(client):

    resp = await client.get('/ping')

    assert resp.status == 200

    assert (await resp.text()) == 'pong'
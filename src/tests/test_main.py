async def test_hello(unauthorized_client):

    resp = await unauthorized_client.get('/')
    assert resp.status == 200

async def test_ping(unauthorized_client):

    resp = await unauthorized_client.get('/ping')

    assert resp.status == 200

    assert (await resp.text()) == 'pong'
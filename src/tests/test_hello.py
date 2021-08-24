async def test_hello(unauthorized_client):

    resp = await unauthorized_client.get('/')
    assert resp.status == 200

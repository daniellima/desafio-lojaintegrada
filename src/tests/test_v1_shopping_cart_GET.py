async def test_get_empty_shopping_cart(client):

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [],
        'coupons': [],
        'subtotal': 0,
        'total': 0
    }

async def test_get_empty_shopping_cart_without_api_key_result_in_error(unauthorized_client):

    resp = await unauthorized_client.get('/v1/shopping_cart')

    assert resp.status == 403

    assert (await resp.json()) == {}
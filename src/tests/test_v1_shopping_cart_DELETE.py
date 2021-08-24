async def test_clear_shopping_cart_should_be_a_success(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 2
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '5',
        'name': 'Playstation 5',
        'price': 3000
    }

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '6',
        'quantity': 3
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '6',
        'name': 'Nintendo Switch',
        'price': 2000
    }

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '103'
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '103',
        'name': 'Desconto Que Nunca Vai Existir Na Realidade',
        'amount': 10000
    }

    resp = await client.delete('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {}

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [],
        'coupons': [],
        'subtotal': 0,
        'total': 0
    }
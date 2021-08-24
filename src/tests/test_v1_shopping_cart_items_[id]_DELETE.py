async def test_remove_item_from_shopping_cart_should_be_a_success(client):

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

    resp = await client.delete('/v1/shopping_cart/items/5')

    assert resp.status == 200

    assert (await resp.json()) == {}

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [
            {
                'id': '6',
                'name': 'Nintendo Switch',
                'price': 2000,
                'quantity': 3
            } 
        ],
        'coupons': [],
        'subtotal': 6000,
        'total': 6000
    }

async def test_remove_item_from_shopping_cart_when_item_dont_exist_should_be_a_success(client):

    resp = await client.delete('/v1/shopping_cart/items/999')

    assert resp.status == 200

    assert (await resp.json()) == {}
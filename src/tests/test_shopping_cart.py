async def test_get_empty_shopping_cart(client):

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [],
        'coupons': [],
        'subtotal': 0,
        'total': 0
    }

async def test_add_item_to_empty_shopping_cart_should_be_a_success(client):

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

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [
            {
                'id': '5',
                'name': 'Playstation 5',
                'price': 3000,
                'quantity': 2
            }
        ],
        'coupons': [],
        'subtotal': 6000,
        'total': 6000
    }

async def test_add_unknow_item_to_shopping_cart_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '999',
        'quantity': 2
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'item_not_found',
            'message': 'Item with id "999" was not found'
        }
    }

async def test_add_item_to_shopping_cart_with_quantity_greater_than_stock_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 1000
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'out_of_stock',
            'message': 'Item with id "5" don\'t have 1000 or more itens in stock'
        }
    }

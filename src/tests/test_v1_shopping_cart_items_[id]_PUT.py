
async def test_update_quantity_of_item_should_be_a_success(client):

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

    resp = await client.put('/v1/shopping_cart/items/5', json={
        'quantity': 5
    })

    assert resp.status == 200

    assert (await resp.json()) == {}

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [
            {
                'id': '5',
                'name': 'Playstation 5',
                'price': 3000,
                'quantity': 5
            }
        ],
        'coupons': [],
        'subtotal': 15000,
        'total': 15000
    }

async def test_update_quantity_of_unknow_item_should_result_in_error(client):

    resp = await client.put('/v1/shopping_cart/items/999', json={
        'quantity': 1
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'item_not_found',
            'message': 'Item with id "999" was not found'
        }
    }

async def test_update_quantity_of_existing_item_not_in_shopping_cart_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 1
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '5',
        'name': 'Playstation 5',
        'price': 3000
    }

    resp = await client.put('/v1/shopping_cart/items/6', json={
        'quantity': 1
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'item_not_found',
            'message': 'Item with id "6" was not found'
        }
    }

async def test_update_quantity_of_item_with_quantity_greater_than_stock_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 1
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '5',
        'name': 'Playstation 5',
        'price': 3000
    }

    resp = await client.put('/v1/shopping_cart/items/5', json={
        'quantity': 1000
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'out_of_stock',
            'message': 'Item with id "5" don\'t have 1000 or more itens in stock'
        }
    }

async def test_update_quantity_of_item_with_empty_body_should_result_in_error(client):

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

    resp = await client.put('/v1/shopping_cart/items/5', json={})

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'failed_validating_json',
            'message': 'Missing key: \'quantity\''
        }
    }

async def test_update_quantity_of_item_with_zero_quantity_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 1
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '5',
        'name': 'Playstation 5',
        'price': 3000
    }

    resp = await client.put('/v1/shopping_cart/items/5', json={
        'quantity': 0
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'failed_validating_json',
            'message': 'Key \'quantity\' must be greater than 0'
        }
    }

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

async def test_add_item_twice_to_shopping_cart_should_result_in_error(client):

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

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '5',
        'quantity': 1
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'item_already_exists_on_shopping_cart',
            'message': 'Item with id "5" is already on this shopping cart'
        }
    }

async def test_add_item_to_shopping_cart_with_empty_body_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={})

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'failed_validating_json',
            'message': 'Missing keys: \'id\', \'quantity\''
        }
    }

async def test_add_item_to_shopping_cart_with_no_quantity_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '10',
        'quantity': 0
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'failed_validating_json',
            'message': 'Key \'quantity\' must be greater than 0'
        }
    }

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

async def test_add_coupon_to_empty_shopping_cart_should_be_a_success(client):

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '100'
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '100',
        'name': 'Desconto Dia dos Pais',
        'amount': 30
    }

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [],
        'coupons': [
            {
                'id': '100',
                'name': 'Desconto Dia dos Pais',
                'amount': 30
            }
        ],
        'subtotal': 0,
        'total': 0
    }

async def test_add_coupon_to_shopping_cart_should_reduce_total(client):

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

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '100'
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '100',
        'name': 'Desconto Dia dos Pais',
        'amount': 30
    }

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '101'
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '101',
        'name': 'Desconto Dia das Mães',
        'amount': 40
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
        'coupons': [
            {
                'id': '100',
                'name': 'Desconto Dia dos Pais',
                'amount': 30
            },
            {
                'id': '101',
                'name': 'Desconto Dia das Mães',
                'amount': 40
            }
        ],
        'subtotal': 6000,
        'total': 5930
    }

async def test_add_coupon_to_shopping_cart_should_not_allow_total_to_be_below_zero(client):

    resp = await client.post('/v1/shopping_cart/items', json={
        'id': '6',
        'quantity': 2
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

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [
            {
                'id': '6',
                'name': 'Nintendo Switch',
                'price': 2000,
                'quantity': 2
            }
        ],
        'coupons': [
            {
                'id': '103',
                'name': 'Desconto Que Nunca Vai Existir Na Realidade',
                'amount': 10000
            }
        ],
        'subtotal': 4000,
        'total': 0
    }

async def test_add_unknow_coupon_to_shopping_cart_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '999'
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'coupon_not_found',
            'message': 'Coupon with id "999" was not found'
        }
    }

async def test_add_coupon_twice_to_shopping_cart_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '100',
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '100',
        'name': 'Desconto Dia dos Pais',
        'amount': 30
    }

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '100',
    })

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'coupon_already_exists_on_shopping_cart',
            'message': 'Coupon with id "100" is already on this shopping cart'
        }
    }

async def test_add_coupon_to_shopping_cart_with_empty_body_should_result_in_error(client):

    resp = await client.post('/v1/shopping_cart/coupons', json={})

    assert resp.status == 400

    assert (await resp.json()) == {
        'error': {
            'type': 'failed_validating_json',
            'message': 'Missing key: \'id\''
        }
    }

async def test_remove_coupon_from_shopping_cart_should_be_a_success(client):

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '100',
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '100',
        'name': 'Desconto Dia dos Pais',
        'amount': 30
    }

    resp = await client.post('/v1/shopping_cart/coupons', json={
        'id': '101'
    })

    assert resp.status == 201

    assert (await resp.json()) == {
        'id': '101',
        'name': 'Desconto Dia das Mães',
        'amount': 40
    }

    resp = await client.delete('/v1/shopping_cart/coupons/100')

    assert resp.status == 200

    assert (await resp.json()) == {}

    resp = await client.get('/v1/shopping_cart')

    assert resp.status == 200

    assert (await resp.json()) == {
        'items': [],
        'coupons': [
            {
                'id': '101',
                'name': 'Desconto Dia das Mães',
                'amount': 40
            }
        ],
        'subtotal': 0,
        'total': 0
    }

async def test_remove_coupon_from_shopping_cart_when_coupon_dont_exist_should_be_a_success(client):

    resp = await client.delete('/v1/shopping_cart/coupons/999')

    assert resp.status == 200

    assert (await resp.json()) == {}

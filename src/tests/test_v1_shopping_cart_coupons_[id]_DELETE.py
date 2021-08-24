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

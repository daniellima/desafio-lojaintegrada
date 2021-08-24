from aiohttp import web
import aiomysql
from src.app.shopping_cart.shopping_cart import ShoppingCart
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
import pytest
from src.app.main import make_app

@pytest.fixture
async def client(aiohttp_client):
    
    app = make_app()

    client = await aiohttp_client(app, headers={
        'X-API-Key': '1234567890'
    })

    return client

@pytest.fixture
async def unauthorized_client(aiohttp_client):
    
    app = make_app()

    client = await aiohttp_client(app)

    return client

@pytest.fixture(autouse=True)
async def empty_shopping_cart():

    async with aiomysql.connect(host='db', port=3306,
                                user='root', password='defaultpass', db='shopping_cart') as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM shopping_cart_item")
            await cur.execute("DELETE FROM shopping_cart_coupon")
            await cur.execute("DELETE FROM shopping_cart")
        
        await conn.commit()
from aiohttp import web
import aiomysql
from src.app.shopping_cart.shopping_cart import ShoppingCart
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
import pytest
from src.app.main import make_app

@pytest.fixture
def client(loop, aiohttp_client):
    
    app = make_app()

    return loop.run_until_complete(aiohttp_client(app))

@pytest.fixture(autouse=True)
async def empty_shopping_cart():

    async with aiomysql.connect(host='db', port=3306,
                                user='root', password='defaultpass', db='shopping_cart') as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM shopping_cart_item")
            await cur.execute("DELETE FROM shopping_cart")
        
        await conn.commit()
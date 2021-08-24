from aiohttp import web
import aiomysql
import pytest
import os
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
    db = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    async with aiomysql.connect(host=host, port=int(port),
                                user=user, 
                                password=password, 
                                db=db) as conn:
    
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM shopping_cart_item")
            await cur.execute("DELETE FROM shopping_cart_coupon")
            await cur.execute("DELETE FROM shopping_cart")
        
        await conn.commit()
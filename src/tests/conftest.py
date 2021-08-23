from aiohttp import web
from src.app.shopping_cart.shopping_cart import ShoppingCart
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
import pytest
from src.app.main import make_app

@pytest.fixture
def client(loop, aiohttp_client):
    
    app = make_app()

    return loop.run_until_complete(aiohttp_client(app))

@pytest.fixture(autouse=True)
def empty_shopping_cart():
    ShoppingCartRepository.sc = ShoppingCart()
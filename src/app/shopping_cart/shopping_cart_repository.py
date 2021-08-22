from src.app.shopping_cart.shopping_cart_item import ShoppingCartItem
from src.app.shopping_cart.shopping_cart import ShoppingCart

sc = ShoppingCart()

class ShoppingCartRepository:

    async def get(self):
        return sc

    async def add_item(self, new_item, quantity):
        item = ShoppingCartItem(new_item, quantity)

        sc.items.append(item)
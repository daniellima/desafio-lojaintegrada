from src.app.shopping_cart.item_already_exists_on_shopping_cart import ItemAlreadyExistsOnShoppingCart
from src.app.shopping_cart.shopping_cart_item import ShoppingCartItem
from src.app.shopping_cart.shopping_cart import ShoppingCart

class ShoppingCartRepository:

    sc = ShoppingCart()

    async def get(self):
        return self.__class__.sc

    async def add_item(self, new_item, quantity):
        item = ShoppingCartItem(new_item, quantity)    

        self.__class__.sc.items.append(item)
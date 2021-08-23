from src.app.database_repository import DatabaseRepository
from src.app.shopping_cart.item_already_exists_on_shopping_cart import ItemAlreadyExistsOnShoppingCart
from src.app.shopping_cart.shopping_cart_item import ShoppingCartItem
from src.app.shopping_cart.shopping_cart import ShoppingCart

class ShoppingCartRepository(DatabaseRepository):

    async def get(self):
        db_cart = await self.query('SELECT id FROM shopping_cart WHERE id = %s', (1,))
        if len(db_cart) == 0:
            await self.update('INSERT INTO shopping_cart VALUES (%s)', (1,))
            db_cart = ({'id': 1},)

        db_cart_id = db_cart[0]['id']

        db_items = await self.query('SELECT id, name, price, quantity FROM shopping_cart_item WHERE shopping_cart_id = %s', (db_cart_id,))

        sc = ShoppingCart()
        sc.id = db_cart_id

        for db_item in db_items:
            sc_item = ShoppingCartItem(str(db_item['id']), db_item['name'], db_item['price'], db_item['quantity'])
            sc.items.append(sc_item)

        return sc

    async def add_item(self, shopping_cart_id, new_item, quantity):
        await self.update('INSERT INTO shopping_cart_item VALUES (%s, %s, %s, %s, %s)', (new_item.id, shopping_cart_id, new_item.name, new_item.price, quantity))

    async def remove_item(self, shopping_cart_id, item_id):
        await self.update('DELETE FROM shopping_cart_item WHERE shopping_cart_id=%s AND id=%s', (shopping_cart_id, item_id))
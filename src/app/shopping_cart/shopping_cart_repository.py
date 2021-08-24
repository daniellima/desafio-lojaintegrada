import json
from src.app.shopping_cart.shopping_cart_coupon import ShoppingCartCoupon
from src.app.database_repository import DatabaseRepository
from src.app.shopping_cart.item_already_exists_on_shopping_cart import ItemAlreadyExistsOnShoppingCart
from src.app.shopping_cart.shopping_cart_item import ShoppingCartItem
from src.app.shopping_cart.shopping_cart import ShoppingCart
import logging

logger = logging.getLogger(__name__)

class ShoppingCartRepository(DatabaseRepository):

    async def get(self, shoping_cart_id):
        db_cart = await self.query('SELECT id FROM shopping_cart WHERE id = %s', (shoping_cart_id,))
        if len(db_cart) == 0:
            await self.update('INSERT INTO shopping_cart VALUES (%s)', (shoping_cart_id,))
            db_cart = ({'id': shoping_cart_id},)

        db_cart_id = db_cart[0]['id']

        sc = ShoppingCart()
        sc.id = db_cart_id

        db_items = await self.query('SELECT id, name, price, quantity FROM shopping_cart_item WHERE shopping_cart_id = %s', (db_cart_id,))

        for db_item in db_items:
            sc_item = ShoppingCartItem(str(db_item['id']), db_item['name'], db_item['price'], db_item['quantity'])
            sc.items.append(sc_item)

        db_coupons = await self.query('SELECT id, name, amount FROM shopping_cart_coupon WHERE shopping_cart_id = %s', (db_cart_id,))

        for db_coupon in db_coupons:
            sc_coupon = ShoppingCartCoupon(str(db_coupon['id']), db_coupon['name'], db_coupon['amount'])
            sc.coupons.append(sc_coupon)

        return sc

    async def clear(self, shopping_cart_id):
        conn = self.conn

        try:
            async with conn.cursor() as cur:
                await self.execute(cur, 'DELETE FROM shopping_cart_item WHERE shopping_cart_id=%s', (shopping_cart_id,))
                await self.execute(cur, 'DELETE FROM shopping_cart_coupon WHERE shopping_cart_id=%s', (shopping_cart_id,))
                
            await conn.commit()
        except Exception as ex:
            logger.error(json.dumps({'message': 'Rollback when executing queries to clear the shopping cart', 'error':str(ex.__class__), 'error_message': str(ex)}, indent=2))
            await conn.rollback()
            raise

    async def add_item(self, shopping_cart_id, new_item, quantity):
        await self.update('INSERT INTO shopping_cart_item VALUES (%s, %s, %s, %s, %s)', (new_item.id, shopping_cart_id, new_item.name, new_item.price, quantity))

    async def remove_item(self, shopping_cart_id, item_id):
        await self.update('DELETE FROM shopping_cart_item WHERE shopping_cart_id=%s AND id=%s', (shopping_cart_id, item_id))

    async def update_item_quantity(self, shopping_cart_id, item_id, new_quantity):
        await self.update('UPDATE shopping_cart_item SET quantity=%s WHERE shopping_cart_id=%s AND id=%s', (new_quantity, shopping_cart_id, item_id))

    async def add_coupon(self, shopping_cart_id, new_coupon):
        await self.update('INSERT INTO shopping_cart_coupon VALUES (%s, %s, %s, %s)', (new_coupon.id, shopping_cart_id, new_coupon.name, new_coupon.amount))

    async def remove_coupon(self, shopping_cart_id, coupon_id):
        await self.update('DELETE FROM shopping_cart_coupon WHERE shopping_cart_id=%s AND id=%s', (shopping_cart_id, coupon_id))
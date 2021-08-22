from src.app.item.item import Item

items = [
    Item(id='5', name='Playstation 5', price=3000)
]

class ItemRepository:

    async def get_by_id(self, item_id):

        for item in items:
            if item.id == item_id:
                return item
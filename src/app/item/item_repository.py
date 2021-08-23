from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.item.item import Item

items = [
    Item(id='5', name='Playstation 5', price=3000, stock=5),
    Item(id='6', name='Nintendo Switch', price=2000, stock=10)
]

class ItemRepository:

    async def get_by_id(self, item_id):

        for item in items:
            if item.id == item_id:
                return item
        
        raise ItemNotFoundException(f'Item with id "{item_id}" was not found')
class ShoppingCartItem:

    def __init__(self, item, quantity):
        self.id = item.id
        self.name = item.name
        self.price = item.price
        self.quantity = quantity

    @property
    def total_price(self):
        return self.price * self.quantity
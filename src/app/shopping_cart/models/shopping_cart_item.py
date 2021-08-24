class ShoppingCartItem:

    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total_price(self):
        return self.price * self.quantity
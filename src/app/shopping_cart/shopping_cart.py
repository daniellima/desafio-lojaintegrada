class ShoppingCart:
    def __init__(self) -> None:
        self.items = []

    @property
    def subtotal(self):
        subtotal = 0
        for sc_item in self.items:
            subtotal += sc_item.total_price
        
        return subtotal

    @property
    def total(self):
        return self.subtotal
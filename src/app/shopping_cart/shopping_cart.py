class ShoppingCart:
    def __init__(self) -> None:
        self.id = None
        self.items = []
        self.coupons = []

    @property
    def subtotal(self):
        subtotal = 0
        for sc_item in self.items:
            subtotal += sc_item.total_price
        
        return subtotal

    @property
    def total_discount(self):
        discount = 0
        for coupon in self.coupons:
            discount += coupon.amount
        
        return discount

    @property
    def total(self):
        return max(0, self.subtotal - self.total_discount)
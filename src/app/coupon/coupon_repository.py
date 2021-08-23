from src.app.coupon.coupon_not_found_exception import CouponNotFoundException
from src.app.coupon.coupon import Coupon

coupons = [
    Coupon(id='100', name='Desconto Dia dos Pais', amount=30),
    Coupon(id='101', name='Desconto Dia das Mães', amount=40),
    Coupon(id='103', name='Desconto Que Nunca Vai Existir Na Realidade', amount=10000)
]

class CouponRepository:

    async def get_by_id(self, coupon_id):

        for coupon in coupons:
            if coupon.id == coupon_id:
                return coupon
        
        raise CouponNotFoundException(f'Coupon with id "{coupon_id}" was not found')
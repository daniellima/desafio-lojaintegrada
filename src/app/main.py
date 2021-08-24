from aiohttp import web
from aiohttp_swagger import setup_swagger
from src.app.shopping_cart.controllers.shopping_cart_coupon_controller import ShoppingCartCouponController
from src.app.shopping_cart.controllers.shopping_cart_item_controller import ShoppingCartItemController
from src.app.shopping_cart.controllers.shopping_cart_controller import ShoppingCartController
import logging
from src.app.shared.middlewares import log_middleware, auth_middleware, error_middleware, db_middleware

logger = logging.getLogger(__name__)

def make_app():

    app = web.Application(middlewares=[log_middleware, auth_middleware, error_middleware, db_middleware])

    app.add_routes([
        web.get('/', hello),
        web.get('/ping', ping),
        web.get('/v1/shopping_cart', ShoppingCartController.get),
        web.delete('/v1/shopping_cart', ShoppingCartController.delete),
        web.post('/v1/shopping_cart/items', ShoppingCartItemController.create),
        web.delete(r'/v1/shopping_cart/items/{id:\d+}', ShoppingCartItemController.delete),
        web.put(r'/v1/shopping_cart/items/{id:\d+}', ShoppingCartItemController.update_quantity),
        web.post('/v1/shopping_cart/coupons', ShoppingCartCouponController.create),
        web.delete(r'/v1/shopping_cart/coupons/{id:\d+}', ShoppingCartCouponController.delete),
    ])

    setup_swagger(app, swagger_template_path='src/app/swagger_template.yaml')

    return app

async def hello(request):
    '''
    ---
    description: Retorna o nome da API de forma estilizada
    tags:
    - misc
    produces:
    - text/plain
    responses:
        "200":
            description: Uma arte ASCII
    '''
    return web.Response(text=r"""
     $$$$$$\  $$\                                     $$\                            $$$$$$\                        $$\            $$$$$$\  $$$$$$$\  $$$$$$\ 
    $$  __$$\ $$ |                                    \__|                          $$  __$$\                       $$ |          $$  __$$\ $$  __$$\ \_$$  _|
    $$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$\ $$$$$$$\   $$$$$$\        $$ /  \__| $$$$$$\   $$$$$$\  $$$$$$\         $$ /  $$ |$$ |  $$ |  $$ |  
    \$$$$$$\  $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ |$$  __$$\ $$  __$$\       $$ |       \____$$\ $$  __$$\ \_$$  _|        $$$$$$$$ |$$$$$$$  |  $$ |  
     \____$$\ $$ |  $$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ |$$ /  $$ |      $$ |       $$$$$$$ |$$ |  \__|  $$ |          $$  __$$ |$$  ____/   $$ |  
    $$\   $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |      $$ |  $$\ $$  __$$ |$$ |        $$ |$$\       $$ |  $$ |$$ |        $$ |  
    \$$$$$$  |$$ |  $$ |\$$$$$$  |$$$$$$$  |$$$$$$$  |$$ |$$ |  $$ |\$$$$$$$ |      \$$$$$$  |\$$$$$$$ |$$ |        \$$$$  |      $$ |  $$ |$$ |      $$$$$$\ 
     \______/ \__|  \__| \______/ $$  ____/ $$  ____/ \__|\__|  \__| \____$$ |       \______/  \_______|\__|         \____/       \__|  \__|\__|      \______|
                                 $$ |      $$ |                    $$\   $$ |                                                                                
                                 $$ |      $$ |                    \$$$$$$  |                                                                                
                                 \__|      \__|                     \______/                                                                                 
    """)

async def ping(request):
    '''
    ---
    description: Retorna um texto fixo e sempre 200. Serve para verificar que a API está funcionando. Útil para monitoramento
    tags:
    - misc
    produces:
    - text/plain
    responses:
        "200":
            description: A string 'pong'.
    '''
    return web.Response(text='pong')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s - %(name)s: %(message)s')

    app = make_app()

    web.run_app(app)
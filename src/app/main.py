from aiohttp import web
from aiohttp_swagger import setup_swagger
from src.app.database_repository import DatabaseRepository
from schema import SchemaError
import aiomysql
from src.app.shopping_cart.item_already_exists_on_shopping_cart import ItemAlreadyExistsOnShoppingCart
from src.app.shopping_cart.out_of_stock_exception import OutOfStockException
from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.shopping_cart.shopping_cart_controller import ShoppingCartController
import logging
import json

logger = logging.getLogger(__name__)

@web.middleware
async def log_middleware(request, handler):
    logger.debug(json.dumps({'message': 'Request received', 'raw':(await request.text())}, indent=2))

    resp = await handler(request)

    if isinstance(resp, web.FileResponse):
        raw_resp = '<file response>'
    else:
        raw_resp = resp.text

    logger.debug(json.dumps({'message': 'Response sent', 'raw':raw_resp}, indent=2))

    return resp

@web.middleware
async def db_middleware(request, handler):
    async with aiomysql.connect(host='db', port=3306,
                                user='root', password='defaultpass', db='shopping_cart') as conn:

        request['conn'] = conn

        return await handler(request)

@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except ItemNotFoundException as ex:
        return web.json_response({
            'error': {
                'type': 'item_not_found',
                'message': str(ex)
            }
        }, status=400)
    except OutOfStockException as ex:
        return web.json_response({
            'error': {
                'type': 'out_of_stock',
                'message': str(ex)
            }
        }, status=400)
    except ItemAlreadyExistsOnShoppingCart as ex:
        return web.json_response({
            'error': {
                'type': 'item_already_exists_on_shopping_cart',
                'message': str(ex)
            }
        }, status=400)
    except SchemaError as ex:
        return web.json_response({
            'error': {
                'type': 'failed_validating_json',
                'message': str(ex.code)
            }
        }, status=400)
    except:
        raise

def make_app():

    app = web.Application(middlewares=[log_middleware, error_middleware, db_middleware])

    app.add_routes([
        web.get('/', hello),
        web.get('/ping', ping),
        web.get('/v1/shopping_cart', ShoppingCartController.get),
        web.post('/v1/shopping_cart/items', ShoppingCartController.post_item),
        web.delete(r'/v1/shopping_cart/items/{id:\d+}', ShoppingCartController.delete_item)
    ])

    setup_swagger(app)

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
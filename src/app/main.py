from aiohttp import web
from aiohttp_swagger import setup_swagger
from src.app.shopping_cart.out_of_stock_exception import OutOfStockException
from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.shopping_cart.shopping_cart_controller import ShoppingCartController

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
    except:
        raise

def make_app():

    app = web.Application(middlewares=[error_middleware])

    app.add_routes([
        web.get('/', hello),
        web.get('/ping', ping),
        web.get('/v1/shopping_cart', ShoppingCartController.get),
        web.post('/v1/shopping_cart/items', ShoppingCartController.post_item)
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
    app = make_app()

    web.run_app(app)
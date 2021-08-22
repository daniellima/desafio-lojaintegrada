from aiohttp import web
from aiohttp_swagger import setup_swagger
from src.app.shopping_cart.shopping_cart_controller import ShoppingCartController

def setup_app(app):

    app.add_routes([
        web.get('/', hello),
        web.get('/ping', ping),
        web.get('/v1/shopping_cart', ShoppingCartController.get),
        web.post('/v1/shopping_cart/items', ShoppingCartController.post_item)
    ])

    setup_swagger(app)

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
    app = web.Application()

    setup_app(app)

    web.run_app(app)
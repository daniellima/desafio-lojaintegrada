from aiohttp import web
from aiohttp_swagger import setup_swagger

def setup_app(app):

    app.add_routes([
        web.get('/', hello),
        web.get('/ping', ping)
    ])

    setup_swagger(app)

async def hello(request):
    '''
    ---
    description: Retorna um "Hello World" no estilo do JSON
    tags:
    - hello word
    produces:
    - application/json
    responses:
        "200":
            description: Se considere bem vindo.
    '''
    return web.json_response({'hello': 'world!'})

async def ping(request):
    return web.Response(text='pong')

if __name__ == '__main__':
    app = web.Application()

    setup_app(app)

    web.run_app(app)
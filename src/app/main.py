from aiohttp import web
from aiohttp_swagger import setup_swagger

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

app = web.Application()

app.add_routes([
    web.get('/', hello)
])

setup_swagger(app)

if __name__ == '__main__':
    web.run_app(app)
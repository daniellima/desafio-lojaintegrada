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
    description: Retorna o nome da API de forma estilizada
    tags:
    - misc
    produces:
    - text/plain
    responses:
        "200":
            description: Uma arte ASCII
    '''
    return web.Response(text="""
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
    return web.Response(text='pong')

if __name__ == '__main__':
    app = web.Application()

    setup_app(app)

    web.run_app(app)
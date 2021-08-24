from aiohttp import web
import aiomysql
import os
from src.app.shared.json_log import log_debug
from schema import SchemaError
from src.app.shopping_cart.exceptions.coupon_already_exists_on_shopping_cart_exception import CouponAlreadyExistsOnShoppingCartException
from src.app.shopping_cart.exceptions.item_already_exists_on_shopping_cart_exception import ItemAlreadyExistsOnShoppingCartException
from src.app.shopping_cart.exceptions.out_of_stock_exception import OutOfStockException
from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.coupon.coupon_not_found_exception import CouponNotFoundException
import logging


logger = logging.getLogger(__name__)

@web.middleware
async def auth_middleware(request, handler):

    key = request.headers.get('X-API-Key', None)

    if request.path.startswith('/v1/shopping_cart'):
        if key is None:
            return web.json_response({}, status=403)
        else:
            # Para simplficar. Como isso funciona na prática depende da estratégia de autenticação de microserviços usada (API Gateway, serviço externo, etc...)
            request['user_id'] = key

        log_debug(logger, {'message': 'Authenticating with API Key', 'key':key})

    return await handler(request)

@web.middleware
async def log_middleware(request, handler):
    log_debug(logger, {'message': 'Request received', 'raw':(await request.text())})

    resp = await handler(request)

    if isinstance(resp, web.FileResponse):
        raw_resp = '<file response>'
    else:
        raw_resp = resp.text

    log_debug(logger, {'message': 'Response sent', 'raw':raw_resp})

    return resp

@web.middleware
async def db_middleware(request, handler):
    db = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    async with aiomysql.connect(host=host, port=int(port),
                                user=user, 
                                password=password, 
                                db=db) as conn:

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
    except CouponNotFoundException as ex:
        return web.json_response({
            'error': {
                'type': 'coupon_not_found',
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
    except ItemAlreadyExistsOnShoppingCartException as ex:
        return web.json_response({
            'error': {
                'type': 'item_already_exists_on_shopping_cart',
                'message': str(ex)
            }
        }, status=400)
    except CouponAlreadyExistsOnShoppingCartException as ex:
        return web.json_response({
            'error': {
                'type': 'coupon_already_exists_on_shopping_cart',
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
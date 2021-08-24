from aiohttp import web
import aiomysql
from schema import SchemaError
from src.app.shopping_cart.exceptions.coupon_already_exists_on_shopping_cart_exception import CouponAlreadyExistsOnShoppingCartException
from src.app.shopping_cart.exceptions.item_already_exists_on_shopping_cart_exception import ItemAlreadyExistsOnShoppingCartException
from src.app.shopping_cart.exceptions.out_of_stock_exception import OutOfStockException
from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.coupon.coupon_not_found_exception import CouponNotFoundException
import logging
import json


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

        logger.debug(json.dumps({'message': 'Authenticating with API Key', 'key':key}, indent=2))

    return await handler(request)

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
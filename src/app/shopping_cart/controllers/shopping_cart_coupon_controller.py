from aiohttp import web
from src.app.shopping_cart.exceptions.coupon_already_exists_on_shopping_cart_exception import CouponAlreadyExistsOnShoppingCartException
from src.app.coupon.coupon_repository import CouponRepository
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
from schema import Schema, And

class ShoppingCartCouponController:

    async def create(request):
        '''
        ---
        description: Adiciona um cupom de desconto no carrinho
        tags:
        - shopping_cart
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: O id do cupom a ser adicionado
          schema:
            type: object
            properties:
              id:
                type: string
                description: O id do cupom a ser adicionado
                example: '100'
            required:
              - id
        responses:
            "201":
                description: Cupom adicionado no carrinho
                schema:
                    type: object
                    properties:
                        id:
                            type: string
                            description: O id do cupom
                            example: '3'
                        name:
                            type: string
                            description: O nome que identifica o cupom para o usuário
                            example: Dia dos Pais
                        amount:
                            type: int
                            description: O valor do desconto que o cupom fornece
                            example: 100
                    required:
                        - id
                        - name
                        - amount
            "400":
                description: O cupom não pode ser adicionado no carrinho. Mais detalhes no erro específico lançado
                schema:
                    type: object
                    properties:
                        error:
                            type: object
                            properties:
                                type:
                                    type: string
                                    description: o tipo do erro
                                    example: no_stock
                                message:
                                    type: string
                                    description: uma descrição legível por humanos para o erro
                                    example: Not enough items in stock
                            required:
                            - type
                            - message
                    required:
                    - error
        '''

        data = await request.json()

        Schema({
            'id': str,
        }).validate(data)

        new_coupon = await CouponRepository().get_by_id(data['id'])

        sc_repo = ShoppingCartRepository(request['conn'])

        sc = await sc_repo.get(request['user_id'])

        already_exists = (new_coupon.id in [coupon.id for coupon in sc.coupons])
        if already_exists:
            raise CouponAlreadyExistsOnShoppingCartException(f'Coupon with id "{new_coupon.id}" is already on this shopping cart')

        await sc_repo.add_coupon(sc.id, new_coupon)

        return web.json_response({
            'id': new_coupon.id,
            'name': new_coupon.name,
            'amount': new_coupon.amount,
        }, status=201)

    async def delete(request):
            '''
            ---
            description: Remove um cupom do carrinho do usuário. Se o cupom não existir, nenhum erro será gerado.
            tags:
            - shopping_cart
            produces:
            - application/json
            parameters:
            - in: path
              name: id
              required: true
              type: string
              description: O id do cupom a ser removido
            responses:
                "200":
                    description: Cupom removido ou já não existente
            '''

            sc_repo = ShoppingCartRepository(request['conn'])

            sc = await sc_repo.get(request['user_id'])

            coupon_id = request.match_info['id']

            await sc_repo.remove_coupon(sc.id, coupon_id)

            return web.json_response({}, status=200)
from aiohttp import web
from src.app.item.item_not_found_exception import ItemNotFoundException
from src.app.shopping_cart.exceptions.item_already_exists_on_shopping_cart_exception import ItemAlreadyExistsOnShoppingCartException
from src.app.shopping_cart.exceptions.out_of_stock_exception import OutOfStockException
from src.app.item.item_repository import ItemRepository
from src.app.coupon.coupon_repository import CouponRepository
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
from schema import Schema, And

class ShoppingCartItemController:

    async def create(request):
        '''
        ---
        description: Retorna o carrinho atual do usuário
        tags:
        - shopping_cart_item
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: O id do item a ser adicionado e sua quantidade
          schema:
            type: object
            properties:
              id:
                type: string
                description: O id do item a ser adicionado
                example: '4'
              quantity:
                type: int
                description: A quantidade de itens a serem adicionados. Precisa ser maior que 0
                example: 2
            required:
              - id
              - quantity
        responses:
            "201":
                description: Item adicionado no carrinho
                schema:
                    type: object
                    properties:
                        id:
                            type: string
                            description: O id do item
                            example: '3'
                        name:
                            type: string
                            description: O nome que identifica o produto para o usuário
                            example: Playstation 5
                        price:
                            type: int
                            description: O preço do produto no momento da adição dele no carrinho
                            example: 5000
                    required:
                        - id
                        - name
                        - price
            "400":
                description: O item não pode ser adicionado no carrinho. Mais detalhes no erro específico lançado
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
            'quantity': And(int, lambda n: n > 0, error='Key \'quantity\' must be greater than 0')
        }).validate(data)

        new_item = await ItemRepository().get_by_id(data['id'])

        quantity = data['quantity']
        if new_item.stock < quantity:
            raise OutOfStockException(f'Item with id "{new_item.id}" don\'t have {quantity} or more itens in stock')

        sc_repo = ShoppingCartRepository(request['conn'])

        sc = await sc_repo.get(request['user_id'])

        already_exists = (new_item.id in [item.id for item in sc.items])
        if already_exists:
            raise ItemAlreadyExistsOnShoppingCartException(f'Item with id "{new_item.id}" is already on this shopping cart')

        await sc_repo.add_item(sc.id, new_item, data['quantity'])

        return web.json_response({
            'id': new_item.id,
            'name': new_item.name,
            'price': new_item.price,
        }, status=201)

    async def delete(request):
            '''
            ---
            description: Remove um item do carrinho do usuário. Se o item não existir, nenhum erro será gerado.
            tags:
            - shopping_cart_item
            produces:
            - application/json
            parameters:
            - in: path
              name: id
              required: true
              type: string
              description: O id do item a ser removido
            responses:
                "200":
                    description: Item removido ou já não existente
            '''

            sc_repo = ShoppingCartRepository(request['conn'])

            sc = await sc_repo.get(request['user_id'])

            item_id = request.match_info['id']

            await sc_repo.remove_item(sc.id, item_id)

            return web.json_response({}, status=200)

    async def update_quantity(request):
        '''
        ---
        description: Atualiza a quantidade de um determinado item no carrinho
        tags:
        - shopping_cart_item
        produces:
        - application/json
        parameters:
        parameters:
        - in: path
          name: id
          required: true
          type: string
          description: O id do item cuja quantidade será atualizada
        - in: body
          name: body
          schema:
            type: object
            properties:
              quantity:
                type: int
                description: A nova quantidade de itens. Precisa ser maior que 0
                example: 2
            required:
              - quantity
        responses:
            "201":
                description: Quantidade do item atualizada
            "400":
                description: A quantidade desse item não pode ser atualizada. Mais detalhes no erro específico lançado
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
            'quantity': And(int, lambda n: n > 0, error='Key \'quantity\' must be greater than 0')
        }).validate(data)

        item_id = request.match_info['id']
        new_quantity = data['quantity']

        item = await ItemRepository().get_by_id(item_id)

        if item.stock < new_quantity:
            raise OutOfStockException(f'Item with id "{item.id}" don\'t have {new_quantity} or more itens in stock')

        sc_repo = ShoppingCartRepository(request['conn'])

        sc = await sc_repo.get(request['user_id'])

        item_in_sc = False
        for sc_item in sc.items:
            if sc_item.id == item.id:
                item_in_sc = True
                break
        if not item_in_sc:
            raise ItemNotFoundException(f'Item with id "{item.id}" was not found')

        await sc_repo.update_item_quantity(sc.id, item.id, new_quantity)

        return web.json_response({}, status=200)
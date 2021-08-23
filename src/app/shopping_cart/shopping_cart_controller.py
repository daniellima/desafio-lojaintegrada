from aiohttp import web
from src.app.shopping_cart.item_already_exists_on_shopping_cart import ItemAlreadyExistsOnShoppingCart
from src.app.shopping_cart.out_of_stock_exception import OutOfStockException
from src.app.item.item_repository import ItemRepository
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository
from schema import Schema, And

class ShoppingCartController:

    async def get(request):
        '''
        ---
        description: Retorna o carrinho atual do usuário
        tags:
        - shopping_cart
        produces:
        - application/json
        responses:
            "200":
                description: O carrinho atual, com os produtos e cupons
                schema:
                    type: object
                    properties:
                        items:
                            type: array
                            description: A lista de produtos no carrinho
                            items:
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
                                    quantity:
                                        type: int
                                        description: Quantos desse produto estão no carrinho
                                        example: 1
                                required:
                                    - id
                                    - name
                                    - price
                                    - quantity
                        coupons:
                            type: array
                            description: A lista de cupons no carrinho
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                        description: O id do cupom
                                        example: '3'
                                    name:
                                        type: string
                                        description: O nome que identifica o cupom para o usuário
                                        example: Desconto Dia dos Pais
                                    amount:
                                        type: int
                                        description: Quanto de desconto o cupom dá
                                        example: 1000
                                required:
                                    - id
                                    - name
                                    - amount
                        subtotal:
                            type: int
                            description: O subtotal do carrinho. É a soma do preço dos produtos, considerando a quantidade dos produtos. Não possui formatação
                            example: 5000
                        total:
                            type: int
                            description: O total do carrinho. É o valor final do carrinho, considerando o subtotal e os cupons de desconto aplicados. Não possui formatação
                            example: 4000
                    required:
                    - items
                    - coupons
                    - subtotal
                    - total
        '''

        sc = await ShoppingCartRepository(request['conn']).get()

        return web.json_response({
            'items': [{
                'id': sc_item.id,
                'name': sc_item.name,
                'price': sc_item.price,
                'quantity': sc_item.quantity
            } for sc_item in sc.items],
            'coupons': [],
            'subtotal': sc.subtotal,
            'total': sc.total
        })

    async def post_item(request):
        '''
        ---
        description: Retorna o carrinho atual do usuário
        tags:
        - shopping_cart
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

        sc = await sc_repo.get()

        already_exists = (new_item.id in [item.id for item in sc.items])
        if already_exists:
            raise ItemAlreadyExistsOnShoppingCart(f'Item with id "{new_item.id}" is already on this shopping cart')

        await sc_repo.add_item(sc.id, new_item, data['quantity'])

        return web.json_response({
            'id': new_item.id,
            'name': new_item.name,
            'price': new_item.price,
        }, status=201)

    async def delete_item(request):
            '''
            ---
            description: Remove um item do carrinho do usuário. Se o item não existir, nenhum erro será gerado.
            tags:
            - shopping_cart
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

            sc = await sc_repo.get()

            item_id = request.match_info['id']

            await sc_repo.remove_item(sc.id, item_id)

            return web.json_response({}, status=200)


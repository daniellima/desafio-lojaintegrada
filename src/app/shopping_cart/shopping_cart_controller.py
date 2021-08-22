from aiohttp import web
from src.app.item.item_repository import ItemRepository
from src.app.shopping_cart.shopping_cart_repository import ShoppingCartRepository

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
                                        description: O id do cupom
                                        example: 3
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
                                        example: 3
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

        sc = await ShoppingCartRepository().get()

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

        # TODO: validation HTTP 

        data = await request.json()

        # TODO: validation negócios (o item já não estã no carrinho. Tem estoque, etc....)

        new_item = await ItemRepository().get_by_id(data['id'])

        await ShoppingCartRepository().add_item(new_item, data['quantity'])

        return web.json_response({
            'id': new_item.id,
            'name': new_item.name,
            'price': new_item.price
        }, status=201)

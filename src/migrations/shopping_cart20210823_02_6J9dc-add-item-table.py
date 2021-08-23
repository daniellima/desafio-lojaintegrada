"""
Add item table
"""

from yoyo import step

__depends__ = {'shopping_cart20210823_01_wQKiM-adding-shopping-cart-table'}

steps = [
    step("""CREATE TABLE shopping_cart_item (
        id INT NOT NULL AUTO_INCREMENT,
        shopping_cart_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        quantity INT NOT NULL,
        PRIMARY KEY ( id, shopping_cart_id ),
        FOREIGN KEY (shopping_cart_id) REFERENCES shopping_cart(id)
    )""",
    """
        DROP TABLE shopping_cart_item
    """)
]

"""
Add coupon table
"""

from yoyo import step

__depends__ = {'shopping_cart20210823_02_6J9dc-add-item-table'}

steps = [
    step("""CREATE TABLE shopping_cart_coupon (
        id INT NOT NULL AUTO_INCREMENT,
        shopping_cart_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        amount INT NOT NULL,
        PRIMARY KEY ( id, shopping_cart_id ),
        FOREIGN KEY (shopping_cart_id) REFERENCES shopping_cart(id)
    )""",
    """
        DROP TABLE shopping_cart_coupon
    """)
]

"""
Adding shopping_cart_table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""CREATE TABLE shopping_cart (
        id INT NOT NULL AUTO_INCREMENT,
        PRIMARY KEY ( id )
    )""",
    """
        DROP TABLE shopping_cart
    """)
]

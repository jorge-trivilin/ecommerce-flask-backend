"""
protocols.py: Cart Management Protocols and Implementations

This module defines protocols and concrete implementations for
handling cart items and cart services.

Protocols:
    - CartItem: A protocol for representing an item in a shopping cart.
    - CartServiceProtocol: A protocol for defining cart-related services.

Classes:
    - ConcreteCartItem: A concrete class implementing the CartItem protocol.

Detailed Description:
    1. CartItem Protocol:
       Defines the structure for items that can be added to or managed within a cart.
       Attributes:
       - product_id (int): The unique identifier for the product.
       - quantity (int): The quantity of the product in the cart.

    2. ConcreteCartItem Class:
       A concrete implementation of the CartItem protocol.
       Attributes:
       - product_id (int): The ID of the product.
       - quantity (int): The quantity of the product.
       Methods:
       - __init__(product_id: int, quantity: int) -> None:
         Initializes a ConcreteCartItem instance.

    3. CartServiceProtocol:
       Defines the interface for cart management services.
       Methods:
       - add_item(user_id: int, product_id: int, quantity: int) -> None:
         Adds an item to the user's cart.
       - remove_item(user_id: int, product_id: int) -> None:
         Removes an item from the user's cart.
       - get_cart(user_id: int) -> List[CartItem]:
         Retrieves the list of items in the user's cart.
       - clear_cart(user_id: int) -> None:
         Clears all items from the user's cart.

Usage:
    - Implement the CartItem protocol to ensure consistency in cart item representations.
    - Implement the CartServiceProtocol to provide a concrete service for managing cart operations.
    - Use ConcreteCartItem when a simple, concrete implementation of CartItem is needed.

This module enhances type safety and provides clear definitions for cart-related functionality,
facilitating the development of robust and maintainable e-commerce systems.
"""

from typing import Protocol, List


class CartItem(Protocol):
    """
    A protocol representing an item in the shopping cart.

    Attributes:
        product_id (int): The ID of the product.
        quantity (int): The quantity of the product in the cart.
    """

    product_id: int
    quantity: int


class ConcreteCartItem:
    """
    A concrete implementation of a cart item.

    Attributes:
        product_id (int): The ID of the product.
        quantity (int): The quantity of the product in the cart.
    """

    def __init__(self, product_id: int, quantity: int) -> None:
        """
        Initializes a new ConcreteCartItem instance.

        Args:
            product_id (int): The ID of the product.
            quantity (int): The quantity of the product in the cart.
        """
        self.product_id = product_id
        self.quantity = quantity


class CartServiceProtocol(Protocol):
    """
    A protocol defining the operations for managing a shopping cart.

    Methods:
        add_item(user_id: int, product_id: int, quantity: int) -> None:
            Adds a product to the user's cart.

        remove_item(user_id: int, product_id: int) -> None:
            Removes a product from the user's cart.

        get_cart(user_id: int) -> List[CartItem]:
            Retrieves all items in the user's cart.

        clear_cart(user_id: int) -> None:
            Clears all items from the user's cart.
    """

    def add_item(self, user_id: int, product_id: int, quantity: int) -> None:
        """
        Adds a product to the user's cart.

        Args:
            user_id (int): The ID of the user.
            product_id (int): The ID of the product.
            quantity (int): The quantity of the product to be added.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def remove_item(self, user_id: int, product_id: int) -> None:
        """
        Removes a product from the user's cart.

        Args:
            user_id (int): The ID of the user.
            product_id (int): The ID of the product to be removed.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def get_cart(self, user_id: int) -> List[CartItem]:
        """
        Retrieves all items in the user's cart.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[CartItem]: A list of items in the cart.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def clear_cart(self, user_id: int) -> None:
        """
        Clears all items from the user's cart.

        Args:
            user_id (int): The ID of the user.
        """
        ...  # pylint: disable=unnecessary-ellipsis

from typing import List, Tuple
from products import Product, LimitedProduct


class Store:
    """A class representing a store containing products."""
    def __init__(self, products: List[Product]):
        """
        Initialize a new store with a list of products.
        products (List[Product]): A list of Product objects in the store.
        """
        self.products = products

    def add_product(self, product: Product):
        """
        Add a product to the store's inventory
        product (Product): the product to add to the store.
        """

        self.products.append(product)

    def remove_product(self, product: Product):
        """
        Remove a product from the store's inventory.
        product (Product): The product to remove from the store.
        """
        self.products = [p for p in self.products if p != product]

    def get_total_quantity(self) -> int:
        """Get the total quantity of all products in the store."""

        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> List[Product]:
        """Get a list of all active products in the store."""

        return [product for product in self.products if product.is_active()]

    @staticmethod
    def calculate_original_price(shopping_list: List[Tuple[Product, int]]) -> float:
        return sum(product.price * quantity for product, quantity in shopping_list)

    @staticmethod
    def calculate_discounted_price(shopping_list: List[Tuple[Product, int]]) -> float:
        """Calculate the total price after applying any promotions."""
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

    def order(self, shopping_list: List[Tuple[Product, int]]) -> str:
        """
        Process an order for multiple products, checking for constraints.
        Raises:
            ValueError: If the quantity ordered exceeds the limit for LimitedProduct.
        """

        for product, quantity in shopping_list:
            if isinstance(product, LimitedProduct) and quantity > product.maximum:
                raise ValueError(f"Cannot order more than {product.maximum} units of {product.name} in one order.")

        original_price = self.calculate_original_price(shopping_list)
        discounted_price = self.calculate_discounted_price(shopping_list)
        savings = original_price - discounted_price

        if savings > 0:
            return (f"Original total price: ${original_price:.2f}\n"
                    f"Total price after promotions: ${discounted_price:.2f}\n"
                    f"You have saved: ${savings:.2f}")
        else:
            return f"Total price: ${discounted_price:.2f}"

    def __contains__(self, product_name):
        """
        Check if a product is available in the store by its name.
        return:
            bool: True if the product is in the store, False otherwise.
        """
        return any(product.name == product_name for product in self.products)

    def __add__(self, other):
        """
        Combine the products of two stores into a new store.
        other (Store): Another Store object.
        return:
            Store: A new Store object with products from both stores.
        """
        new_products = self.products + other.products
        return Store(new_products)

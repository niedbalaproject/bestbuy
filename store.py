from typing import List, Tuple
from products import Product, LimitedProduct


class Store:
    def __init__(self, products: List[Product]):
        self.products = products

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product: Product):
        self.products = [p for p in self.products if p != product]

    def get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> List[Product]:
        return [product for product in self.products if product.is_active()]

    @staticmethod
    def calculate_original_price(shopping_list: List[Tuple[Product, int]]) -> float:
        return sum(product.price * quantity for product, quantity in shopping_list)

    @staticmethod
    def calculate_discounted_price(shopping_list: List[Tuple[Product, int]]) -> float:
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

    def order(self, shopping_list: List[Tuple[Product, int]]) -> str:
        # Check for any order constraints, such as quantity limits for LimitedProduct
        for product, quantity in shopping_list:
            if isinstance(product, LimitedProduct) and quantity > product.maximum:
                raise ValueError(f"Cannot order more than {product.maximum} units of {product.name} in one order.")

        original_price = self.calculate_original_price(shopping_list)
        discounted_price = self.calculate_discounted_price(shopping_list)
        savings = original_price - discounted_price

        if savings > 0:
            # Promotions have been applied, show detailed info
            return (f"Original total price: ${original_price:.2f}\n"
                    f"Total price after promotions: ${discounted_price:.2f}\n"
                    f"You have saved: ${savings:.2f}")
        else:
            # No promotions applied, show only total price
            return f"Total price: ${discounted_price:.2f}"

    def __contains__(self, product_name):
        return any(product.name == product_name for product in self.products)

    def __add__(self, other):
        new_products = self.products + other.products
        return Store(new_products)

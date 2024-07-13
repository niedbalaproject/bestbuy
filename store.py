from typing import List, Tuple
from bestbuy import products as prod


class Store:
    def __init__(self, products: List[prod.Product]):
        self.products = products

    def add_product(self, product: prod.Product):
        self.products.append(product)

    def remove_product(self, product: prod.Product):
        self.products = [p for p in self.products if p != product]

    def get_total_quantity(self) -> int:
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> List[prod.Product]:
        return [product for product in self.products if product.is_active()]

    @staticmethod
    def order(shopping_list: List[Tuple[prod.Product, int]]) -> float:
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

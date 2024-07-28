from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstract base class for all promotions."""
    def __init__(self, name: str):
        """
        Initialize a promotion.
        name (str): The name of the promotion.
        """

        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the promotion to the given product and quantity.
        product (Product): The product to which the promotion is applied.
        quantity (int): The quantity of the product.
        return: The total price after applying the promotion.
        """
        pass


class PercentageDiscount(Promotion):
    """A promotion offering a percentage discount."""
    def __init__(self, name: str, discount_percent: float):
        """
        Initialize a percentage discount promotion.
        name (str): The name of the promotion.
        discount_percent (float): The discount percentage.
        """
        super().__init__(name)
        self.discount_percent = discount_percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the percentage discount promotion.
        product (Product): The product to which the promotion is applied.
        quantity (int): The quantity of the product.
        return: The total price after applying the discount.
        """
        discount = (self.discount_percent / 100) * product.price
        return product.price * quantity - discount * quantity


class SecondItemHalfPrice(Promotion):
    """A promotion offering the second item at half price."""
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the second item half price promotion.
        product (Product): The product to which the promotion is applied.
        quantity (int): The quantity of the product.
        return: The total price after applying the promotion.
        """
        pairs = quantity // 2
        singles = quantity % 2
        total_price = (pairs * (product.price * 1.5)) + (singles * product.price)
        return total_price


class BuyTwoGetOneFree(Promotion):
    """A promotion offering a free item for every two items purchased."""
    def apply_promotion(self, product, quantity) -> float:
        """Apply the buy two get one free promotion.
        product (Product): The product to which the promotion is applied.
        quantity (int): The quantity of the product.
        return: The total price after applying the promotion."""
        sets_of_three = quantity // 3
        remainder = quantity % 3
        total_price = (sets_of_three * 2 + remainder) * product.price
        return total_price

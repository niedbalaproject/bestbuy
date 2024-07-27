from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class PercentageDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        discount = product.price * (self.percent / 100)
        return product.price * quantity - discount * quantity


class SecondItemHalfPrice(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        if quantity == 1:
            return product.price
        else:
            # calculate number of full price and half price items
            full_price_items = quantity // 2 + quantity % 2
            half_price_items = quantity // 2
            return full_price_items * product.price + half_price_items * (product.price / 2)


class BuyTwoGetOneFree(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        # calculate number of full price sets of 3 and remaining items
        sets_of_three = quantity // 3
        remaining_items = quantity % 3
        return (sets_of_three * 2 + remaining_items) * product.price

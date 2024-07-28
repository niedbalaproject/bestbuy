from abc import ABC, abstractmethod


# Product class and its derived classes
class Product:
    def __init__(self, name, price, quantity):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid parameters for creating a Product.")
        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self):
        return self._active

    @property
    def promotion(self):
        return self._promotion

    @promotion.setter
    def promotion(self, promo):
        self._promotion = promo

    def is_active(self) -> bool:
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def __str__(self) -> str:
        promo_info = f" | Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_info}"

    def buy(self, quantity) -> float:
        if quantity <= 0:
            raise ValueError("You should choose at least 1 item.")
        if not self.active:
            raise Exception(f"Product {self.name} is not active.")
        if quantity > self.quantity:
            raise Exception(f"Not enough quantity available for {self.name}. Available: {self.quantity}, /"
                            f"Requested: {quantity}")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        self.quantity -= quantity
        return total_price

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, 0)

    @property
    def quantity(self):
        return 0

    @quantity.setter
    def quantity(self, value):
        pass  # Prevent setting quantity

    def __str__(self) -> str:
        return f"{self.name}, Price: {self.price} (Non-stocked item)"

    def buy(self, quantity) -> float:
        if quantity <= 0:
            raise ValueError("You should choose at least 1 item.")
        if not self.is_active():
            raise Exception(f"Product {self.name} is not active.")
        return self.price * quantity


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def __str__(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity} (Max per order: {self.maximum})"

    def buy(self, quantity) -> float:
        if quantity > self.maximum:
            raise Exception(f"Cannot buy more than {self.maximum} of {self.name} in one order.")
        return super().buy(quantity)

    def add_to_cart(self, cart, quantity):
        if self not in cart:
            cart[self] = 0

        if cart[self] + quantity > self.maximum:
            raise ValueError(f"Cannot add more than {self.maximum} of {self.name} in total to the cart.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available quantity: {self.quantity}.")

        cart[self] += quantity
        print(f"Added {quantity} of {self.name} to the cart. Total in cart: {cart[self]}.")


# Base class for promotions
class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


# Specific promotion classes
class PercentageDiscount(Promotion):
    def __init__(self, name: str, discount_percent: float):
        super().__init__(name)
        self.discount_percent = discount_percent

    def apply_promotion(self, product, quantity) -> float:
        discount = (self.discount_percent / 100) * product.price
        return product.price * quantity - discount * quantity


class SecondItemHalfPrice(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        pairs = quantity // 2
        singles = quantity % 2
        total_price = (pairs * (product.price * 1.5)) + (singles * product.price)
        return total_price


class BuyTwoGetOneFree(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        sets_of_three = quantity // 3
        remainder = quantity % 3
        total_price = (sets_of_three * 2 * product.price) + (remainder * product.price)
        return total_price

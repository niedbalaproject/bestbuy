class Product:

    def __init__(self, name, price, quantity):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid parameters for creating a Product.")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        print(f"Set quantity for {self.name} to {self.quantity}, active: {self.active}")

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        print(f"{self.name} deactivated")

    def get_promotion(self):
        return self.promotion

    def set_promotion(self, promotion):
        self.promotion = promotion

    def show(self) -> str:
        promotion_str = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promotion_str}"

    def buy(self, quantity) -> float:
        if quantity <= 0:
            raise ValueError("You should choose at least 1 item.")
        if not self.active:
            raise Exception(f"Product {self.name} is not active.")
        if quantity > self.quantity:
            raise Exception(f"Not enough quantity available for {self.name}. /"
                            f"Available: {self.quantity}, Requested: {quantity}")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, 0)

    def set_quantity(self, quantity):
        self.quantity = 0  # quantity always set to zero for non-stocked products

    def get_quantity(self) -> float:
        return 0

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: Non-Stocked"

    def buy(self, quantity: int) -> float:
        return self.price * quantity  # quantity is irrelevant, it should always return price * quantity


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} of {self.name} in one order.")
        return super().buy(quantity)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per oder: {self.maximum}"

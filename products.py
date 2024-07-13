class Product:

    def __init__(self, name, price, quantity):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid parameters for creating a Product.")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        if quantity <= 0:
            raise ValueError("You should choose at least 1 item.")
        if not self.active:
            raise Exception(f"Product {self.name} is not active.")
        if quantity > self.quantity:
            raise Exception(f"Not enough quantity available for {self.name}. /"
                            f"Available: {self.quantity}, Requested: {quantity}")
        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price

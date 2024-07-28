# Product class and its derived classes
class Product:
    """A class representing a generic product."""
    def __init__(self, name, price, quantity):
        """
        Initialize a new product.

        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The quantity available in stock.
        """
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid parameters for creating a Product.")
        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def name(self):
        """Get the product's name."""
        return self._name

    @property
    def price(self):
        """Get the product's price."""
        return self._price

    @property
    def quantity(self):
        """Get the product's quantity in stock."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Set the product's quantity in stock."""
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self):
        """Check if the product is active."""
        return self._active

    @property
    def promotion(self):
        """Set a promotion for the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, promo):
        """Set a promotion for the product."""
        self._promotion = promo

    def is_active(self) -> bool:
        """Determine if the product is active."""
        return self._active

    def activate(self):
        """Activate the product."""
        self._active = True

    def deactivate(self):
        """Deactivate the product."""
        self._active = False

    def __str__(self) -> str:
        """Return a string representation of the product."""
        promo_info = f" | Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_info}"

    def buy(self, quantity) -> float:
        """ Purchase a specified quantity of the product.
        Args: Quantity - the number to buy
        return: The total price for the purchased quantity.
        """

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
        """Less than comparison based on price."""
        return self.price < other.price

    def __gt__(self, other):
        """Greater than comparison based on price."""
        return self.price > other.price


class NonStockedProduct(Product):
    """A class representing a product that is not physically stocked."""
    def __init__(self, name, price):
        """Initialize a non-stocked product.
        name (str): The name of the product.
        price (float): The price of the product.
        """

        super().__init__(name, price, 0)

    @property
    def quantity(self):
        """Get the quantity, always 0 for non-stocked products."""
        return 0

    @quantity.setter
    def quantity(self, value):
        """Prevent setting quantity for non-stocked products."""
        pass

    def __str__(self) -> str:
        """Return a string representation of the product."""
        return f"{self.name}, Price: {self.price} (Non-stocked item)"

    def buy(self, quantity) -> float:
        """Purchase a specified quantity of the product.
        Args: quantity - the number to buy.
        return: The total price for the purchased quantity.
        """

        if quantity <= 0:
            raise ValueError("You should choose at least 1 item.")
        if not self.is_active():
            raise Exception(f"Product {self.name} is not active.")
        return self.price * quantity


class LimitedProduct(Product):
    """A class representing a product with purchase limitations. """
    def __init__(self, name, price, quantity, maximum):
        """
        Initialize a limited product.
        Args:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The quantity available in stock.
        maximum (int): The maximum quantity per order.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def __str__(self) -> str:
        """Return a string representation of the product."""

        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity} (Max per order: {self.maximum})"

    def buy(self, quantity) -> float:
        """
        Purchase a specified quantity of the product.
        quantity: The number to buy.
        return: The total price for the purchased quantity (float).
        """

        if quantity > self.maximum:
            raise Exception(f"Cannot buy more than {self.maximum} of {self.name} in one order.")
        return super().buy(quantity)

    def add_to_cart(self, cart, quantity):
        """
        Add a specified quantity of the product to the cart.
        cart (dict): The shopping cart.
        quantity (int): The number to add.
        """
        if self not in cart:
            cart[self] = 0

        if cart[self] + quantity > self.maximum:
            raise ValueError(f"Cannot add more than {self.maximum} of {self.name} in total to the cart.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock for {self.name}. Available quantity: {self.quantity}.")

        cart[self] += quantity
        print(f"Added {quantity} of {self.name} to the cart. Total in cart: {cart[self]}.")

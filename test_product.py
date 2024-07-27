import pytest
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
from promotions import PercentageDiscount, SecondItemHalfPrice, BuyTwoGetOneFree


# Test Product functionalities
def test_create_product():
    product = Product("Test Product", price=10.0, quantity=100)
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.quantity == 100
    assert product.is_active()


def test_create_product_invalid():
    with pytest.raises(ValueError):
        Product("", price=10.0, quantity=100)
    with pytest.raises(ValueError):
        Product("Test Product", price=-10.0, quantity=100)
    with pytest.raises(ValueError):
        Product("Test Product", price=10.0, quantity=-100)


def test_set_quantity():
    product = Product("Test Product", price=10.0, quantity=100)
    product.set_quantity(50)
    assert product.get_quantity() == 50
    product.set_quantity(0)
    assert not product.is_active()
    with pytest.raises(ValueError):
        product.set_quantity(-10)


def test_buy_product():
    product = Product("Test Product", price=10.0, quantity=100)
    total_price = product.buy(10)
    assert total_price == 100.0
    assert product.get_quantity() == 90
    with pytest.raises(ValueError):
        product.buy(0)
    with pytest.raises(ValueError):
        product.buy(-10)
    with pytest.raises(Exception):
        product.buy(200)


# Test Store functionalities
@pytest.fixture
def store_with_products():
    product1 = Product("Product 1", price=10.0, quantity=100)
    product2 = Product("Product 2", price=20.0, quantity=50)
    product3 = Product("Product 3", price=30.0, quantity=0)
    return Store([product1, product2, product3])


def test_add_product(store_with_products):
    new_product = Product("Product 4", price=40.0, quantity=30)
    store_with_products.add_product(new_product)
    assert new_product in store_with_products.products


def test_remove_product(store_with_products):
    product_to_remove = store_with_products.products[0]
    store_with_products.remove_product(product_to_remove)
    assert product_to_remove not in store_with_products.products


def test_get_total_quantity(store_with_products):
    total_quantity = store_with_products.get_total_quantity()
    assert total_quantity == 150


def test_get_all_products(store_with_products):
    active_products = store_with_products.get_all_products()
    assert len(active_products) == 3  # three products should be active
    assert all(product.is_active() for product in active_products)


def test_order(store_with_products):
    product1, product2, _ = store_with_products.products
    shopping_list = [(product1, 10), (product2, 5)]
    total_price = store_with_products.order(shopping_list)
    assert total_price == 200.0
    assert product1.get_quantity() == 90
    assert product2.get_quantity() == 45
    with pytest.raises(Exception):
        store_with_products.order([(product1, 200)])


# Test NonStockedProduct functionalities
def test_create_non_stocked_product():
    product = NonStockedProduct("Non-Stocked Product", price=200.0)
    assert product.name == "Non-Stocked Product"
    assert product.price == 200.0
    assert product.quantity == 0  # Should always be 0
    assert product.is_active()


def test_non_stocked_product_quantity_handling():
    product = NonStockedProduct("Non-Stocked Product", price=200.0)
    assert product.get_quantity() == 0
    product.set_quantity(10)  # Attempt to set quantity
    assert product.get_quantity() == 0  # Quantity should remain 0


def test_non_stocked_product_buy():
    product = NonStockedProduct("Non-Stocked Product", price=200.0)
    total_price = product.buy(5)
    assert total_price == 1000.0  # 5 items at $200 each
    assert product.get_quantity() == 0  # Quantity remains unaffected


#  Test Promotions
def test_apply_percentage_discount():
    product = Product("Test Product", price=100.0, quantity=100)
    promo = SecondItemHalfPrice("Second item half price")
    product.set_promotion(promo)
    assert product.buy(2) == pytest.approx(150.0)


def test_apply_buy_two_get_one_free():
    product = Product("Test Product", price=100.0, quantity=100)
    promo = BuyTwoGetOneFree("Buy 2 Get 1 Free")
    product.set_promotion(promo)
    assert product.buy(3) == pytest.approx(200.0)


# Additional Store Tests for Promotions
def test_order_with_promotions(store_with_products):
    product1, product2, _ = store_with_products.products
    product1.set_promotion(PercentageDiscount("10% off", 10))
    product2.set_promotion(BuyTwoGetOneFree("Buy 2 Get 1 Free"))
    shopping_list = [(product1, 10), (product2, 3)]
    total_price = store_with_products.order(shopping_list)
    assert total_price == pytest.approx(130.0)  # product 1 total price = 90, total price for product 2 = 40


def test_order_with_limited_products(store_with_products):
    limited_products = LimitedProduct("Limited Product", price=50, quantity=10, maximum=2)
    store_with_products.add_product(limited_products)
    shopping_list = [(limited_products, 2)]
    total_price = store_with_products.order(shopping_list)
    assert total_price == 100.0
    with pytest.raises(ValueError):
        store_with_products.order([(limited_products, 3)])  # should raise an error, limit is 2

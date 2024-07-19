import pytest
from products import Product
from store import Store


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
    assert len(active_products) == 2  # Only two products should be active
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

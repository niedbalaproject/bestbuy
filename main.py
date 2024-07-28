import products as prod
import store
import promotions as promo


def list_products(store_obj):
    """
    Generate a formatted list of products in the store.
    store_obj (store.Store): The store object containing the products.
    """
    product_listings = [f"{i + 1}. {product}" for i, product in enumerate(store_obj.get_all_products())]
    return "\nListing all products:\n" + "\n".join(product_listings)


def show_total_amount(store_obj):
    """Display the total amount of products in the store."""

    total_quantity = store_obj.get_total_quantity()
    return f"\nTotal amount in store: {total_quantity}"


def display_products_with_numbers(store_obj):
    """Display available products with numbers for selection."""
    product_list = store_obj.get_all_products()
    product_list_with_numbers = [f"{i + 1}. {product}" for i, product in enumerate(product_list)]
    for product in product_list_with_numbers:
        print(product)
    return product_list


def select_product(product_list):
    """Select a product by number or name from the displayed list."""
    choice = input("\nEnter the number or part of the name of the product "
                   "you want to buy (or 'done' to finish): ").strip()

    if choice.lower() == 'done':
        return None

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(product_list):
            return product_list[choice_index]
        else:
            print("Invalid product number. Please try again.")
            return select_product(product_list)
    except ValueError:
        matching_products = [product for product in product_list if choice.lower() in product.name.lower()]
        if not matching_products:
            print("No products found with that name. Please try again.")
            return select_product(product_list)
        elif len(matching_products) == 1:
            return matching_products[0]
        else:
            print("Multiple products found:")
            for i, matching_product in enumerate(matching_products, 1):
                print(f"{i}. {matching_product}")
            sub_choice = input("Please enter the number of the product you meant: ").strip()
            try:
                sub_choice_index = int(sub_choice) - 1
                if 0 <= sub_choice_index < len(matching_products):
                    return matching_products[sub_choice_index]
                else:
                    print("Invalid product number. Please try again.")
                    return select_product(product_list)
            except ValueError:
                print("Invalid input. Please enter a valid product number.")
                return select_product(product_list)


def enter_quantity(product, current_quantity_in_cart=0):
    """Enter the quantity for the selected product, considering cart limits."""
    while True:
        try:
            # Determine the maximum quantity that can be added
            if isinstance(product, prod.NonStockedProduct):
                max_quantity = float('inf')  # No stock limit for NonStockedProduct
                available_text = ""  # No need to display available quantity
            elif isinstance(product, prod.LimitedProduct):
                max_quantity = product.maximum - current_quantity_in_cart
                available_text = f" (Max per order: {product.maximum})"
            else:
                max_quantity = product.quantity - current_quantity_in_cart
                available_text = f" (Available: {product.quantity})"

            if max_quantity <= 0:
                print(f"\nNo more {product.name} can be added to the cart due to stock or order limits.\n")
                return 0  # No quantity can be added

            quantity = int(input(f"Enter the quantity for {product.name}{available_text}: "))

            if quantity <= 0:
                print("Quantity should be at least 1. Please try again.")
            elif quantity > max_quantity:
                print(f"Cannot add more than {max_quantity} of {product.name} to the cart. Please try again.")
            else:
                return quantity
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")


def create_shopping_list(store_obj):
    """Create a shopping list based on user input.
    return: A list of tuples, each containing a Product and the desired quantity."""
    shopping_list = []
    product_list = store_obj.get_all_products()

    while True:
        display_products_with_numbers(store_obj)
        selected_product = select_product(product_list)
        if selected_product is None:
            break

        # Check current quantity in cart for this product
        current_quantity_in_cart = sum(qty for item, qty in shopping_list if item == selected_product)

        quantity = enter_quantity(selected_product, current_quantity_in_cart)
        if quantity > 0:
            shopping_list.append((selected_product, quantity))
            print(f"\nProduct {selected_product.name} added to the cart.\n")
    return shopping_list


def place_order(store_obj, shopping_list):
    """
    Place an order and calculate the final cost after promotions.
    return: A summary of the order including original price, discounted price, and savings.
    """
    if not shopping_list:
        return "\nYour cart is empty. You haven't placed any order."

    try:
        original_price = store_obj.calculate_original_price(shopping_list)
        discounted_price = store_obj.calculate_discounted_price(shopping_list)
        savings = original_price - discounted_price

        if savings > 0:
            return (f"\nOriginal total price: ${original_price:.2f}\n"
                    f"Total price after promotions: ${discounted_price:.2f}\n"
                    f"You have saved: ${savings:.2f}")
        else:
            return f"\nTotal price: ${original_price:.2f}"
    except Exception as e:
        return f"Error placing order: {e}"


def make_order(store_obj):
    """
    Main function to create a shopping list and place an order.
    store_obj (store.Store): The store object managing the products.
    return: A summary of the order or an error message if the order fails.
    """
    shopping_list = create_shopping_list(store_obj)
    return place_order(store_obj, shopping_list)


def quit_program():
    """Exit the program."""
    return "Thank you for visiting the store. Goodbye!"


menu_options = [
    ("List all products in store", list_products),
    ("Show total amount in store", show_total_amount),
    ("Make an order", make_order),
    ("Quit", quit_program)
]


def display_menu():
    """
    Generate the main menu.
    return: The formatted menu string.
    """
    menu_lines = []
    for idx, (option, _) in enumerate(menu_options, 1):
        menu_lines.append(f"{idx}. {option}")
    return "\n".join(menu_lines)


def start(store_obj):
    """
    Start the store interaction program
    store_obj (store.Store): The store object managing the products..
    """
    print("\nWelcome to the Store!")
    actions = {
        "1": list_products,
        "2": show_total_amount,
        "3": make_order,
        "4": quit_program
    }

    while True:
        print(display_menu())
        choice = input("\nPlease enter your choice: ")

        if choice not in actions:
            print("Invalid choice, please try again.")
            continue

        action = actions[choice]
        if action == quit_program:
            result = quit_program()
            print(result)
            break
        else:
            result = action(store_obj)
            print(result)

        print("- - - - - - - - - - -\nStore Menu:")


def main():
    """Main function with an initial setup of the store's inventory and promotions."""
    product_list = [
        prod.Product("MacBook Air M2", price=1450, quantity=100),
        prod.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        prod.Product("Google Pixel 7", price=500, quantity=250),
        prod.NonStockedProduct("Windows License", price=125),
        prod.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Adding promotions
    discount_promotion = promo.PercentageDiscount("20% off", 20)
    second_item_half_price = promo.SecondItemHalfPrice("Second item at half price")
    buy_two_get_one_free = promo.BuyTwoGetOneFree("Buy 2, get 1 free")

    product_list[0].promotion = discount_promotion  # MacBook Air M2
    product_list[1].promotion = second_item_half_price  # Bose QuietComfort Earbuds
    product_list[2].promotion = buy_two_get_one_free  # Google Pixel 7

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()

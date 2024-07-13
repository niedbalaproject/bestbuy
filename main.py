import products as prod
import store


def list_products(store_obj):
    """Generate a formatted list of products in the store."""
    product_listings = [f"{i+1}. {product.show()}" for i, product in enumerate(store_obj.get_all_products())]
    return "\nListing all products:\n" + "\n".join(product_listings)


def show_total_amount(store_obj):
    total_quantity = store_obj.get_total_quantity()
    return f"\nTotal amount in store: {total_quantity}"


def get_product_by_name(store_obj, name):
    """Find a product in the store by its name."""
    name = name.lower()
    matches = [product for product in store_obj.get_all_products() if name in product.name.lower()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print("Multiple products found:")
        for match in matches:
            print(f"- {match.name}")
        print("Please enter a full and correct name of the product.")
    return None


def display_products_with_numbers(store_obj):
    """Display available products with numbers."""
    product_list = store_obj.get_all_products()
    product_list_with_numbers = [f"{i + 1}. {product.show()}" for i, product in enumerate(product_list)]
    for product in product_list_with_numbers:
        print(product)
    return product_list


def select_product(product_list):
    """Select a product by number or name."""
    choice = input("\nEnter the number or part of the name of the product you want to buy (or 'done' to finish): ").strip()

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
                print(f"{i}. {matching_product.show()}")
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


def enter_quantity(product):
    """Enter the quantity for the selected product."""
    while True:
        try:
            quantity = int(input(f"Enter the quantity for {product.name} (Available: {product.get_quantity()}): "))
            if quantity <= 0:
                print("Quantity should be at least 1. Please try again.")
            elif quantity > product.get_quantity():
                print(f"Not enough stock. Available quantity: {product.get_quantity()}. Please try again.")
            else:
                return quantity
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")


def create_shopping_list(store_obj):
    """Create a shopping list based on user input."""
    shopping_list = []
    product_list = store_obj.get_all_products()
    while True:
        display_products_with_numbers(store_obj)
        product = select_product(product_list)
        if product is None:
            break
        quantity = enter_quantity(product)
        shopping_list.append((product, quantity))
        print(f"\nProduct {product.name} added to the cart.")
    return shopping_list


def place_order(store_obj, shopping_list):
    """Place an order and handle the output."""
    output = ["\nMaking an order:"]
    if not shopping_list:
        output.append("Your cart is empty. You haven't placed any order.")
    else:
        try:
            total_price = store_obj.order(shopping_list)
            output.append(f"Order placed successfully! Total price: {total_price}")
        except Exception as e:
            output.append(f"Error placing order: {e}")
    return "\n".join(output)


def make_order(store_obj):
    """Main function to create a shopping list and place an order."""
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
    """Generate the main menu."""
    menu_lines = []
    for idx, (option, _) in enumerate(menu_options, 1):
        menu_lines.append(f"{idx}. {option}")
    return "\n".join(menu_lines)


def start(store_obj):
    """Start the program."""
    print("\nWelcome to the Store!")
    actions = {
        "1": list_products,
        "2": store.Store.get_total_quantity,
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
    """Main function with an initial setup of stock of inventory."""
    product_list = [
        prod.Product("MacBook Air M2", price=1450, quantity=100),
        prod.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        prod.Product("Google Pixel 7", price=500, quantity=250),
        prod.Product("Nice Earbuds", price=40, quantity=200)
    ]
    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()

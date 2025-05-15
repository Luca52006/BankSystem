
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

class Product:
    """
    Skapa produkterna och visa upp dom
    """

    def __init__(self, name, description, image, price):
        self.name = name
        self.description = description
        self.image = image
        self.price = price

    def visa_produkter(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Image: {self.image}")
        print(f"Price: ${self.price}")
        print("-" * 40)

class ShoppingCart:
    """"
    Lägger till produkter i kundvagn och kan ta bort dem
    """
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)
        print(f"Added '{product.name}' to cart.")

    def remove(self, index):
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            print(f"Removed '{removed.name}' from cart.")
        else:
            print("Invalid item number.")

    def show(self):
        if not self.items:
            print("Cart is empty.")
        else:
            print("\n--- Shopping Cart ---")
            for i, item in enumerate(self.items, 1):
                print(f"{i}. {item.name} - ${item.price}")
            print("---------------------\n")

def search_products(search_terms):
    query = '&search='.join(search_terms)
    url = (
        f'https://api.bestbuy.com/v1/products(search={query})?format=json&show=sku,name,shortDescription,image,salePrice&apiKey={API_KEY}'
    )

    try:
        response = requests.get(url)
        products = response.json().get("products", [])
        return [
            Product(
                name=item.get("name"),
                description=item.get("shortDescription"),
                image=item.get("image"),
                price=item.get("salePrice"),
            )
            for item in products
        ]
    except Exception as e:
        print(f"Error: {e}")
        return []

def display_products(products):
    for i, product in enumerate(products, 1):
        print(f"Product #{i}")
        product.visa_produkter()

if __name__ == "__main__":
    cart = ShoppingCart()
    while True:
        print(f"""
{"-" * 70}
                [1] 🔍 Search for products
                [2] 🛒 View your cart
                [3] 🗑️ Remove an item from your cart
                [4] 🚪 Quit
{"-" * 70}
              """)

        choice = input("What would you like to do? ").strip()
        if choice == "4":
            break
        elif choice == "2":
            cart.show()
        elif choice == "1":
            search_terms = input("Search: ").split()
            products = search_products(search_terms)

            if not products:
                print("No products found")
                continue
            display_products(products)

            while True:
                choice = input("Enter product number to add to cart (or 'back' to go back): ").strip()
                if choice == "back":
                    break
                if choice.isdigit():
                    ii = int(choice) - 1
                    if 0 <= ii < len(products):
                        cart.add(products[ii])
                    else:
                        print("Invalid number")
                else:
                    print("Not a valid number, try again or type 'back'")
        elif choice == "3":
            cart.show()
            if not cart.items:
                print('Cart is empty')
                continue
            remove_choice = input("Enter item number to remove (or 'back' to cancel): ").strip()
            if remove_choice == "back":
                continue
            if remove_choice.isdigit():
                i = int(remove_choice) - 1
                cart.remove(i)
            else:
                print("Not a valid number, try again or type 'back'")
        else:
            print("Unknown input")

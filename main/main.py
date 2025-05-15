
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
    Lägger till produkter i kundvagn
    """
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)
        print(f"Added '{product.name}' to cart.")

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
    for idx, product in enumerate(products, 1):
        print(f"Product #{idx}")
        product.visa_produkter()

if __name__ == "__main__":
    cart = ShoppingCart()
    while True:
        print("""
              [1] Search for products
              [2] View cart
              [3] Quit
              """)

        choice = input("What do you want to do? ").strip().lower()
        if choice == "3":
            print("Bye!")
            break
        elif choice == "2":
            cart.show()
        elif choice == "1":
            search_terms = input("Search: ").split()
            products = search_products(search_terms)

            if not products:
                print("No products found.")
                continue
            display_products(products)

            while True:
                choice = input("Enter product number to add to cart (or 'back' to go back): ").strip()
                if choice == "back":
                    break
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(products):
                        cart.add(products[idx])
                    else:
                        print("Invalid number.")
                else:
                    print("Please enter a number or 'back'.")
        else:
            print("Unknown command.")

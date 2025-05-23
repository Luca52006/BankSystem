
import requests
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime
from colorama import Fore

load_dotenv()
API_KEY = os.getenv('API_KEY')

CART_FILE = "cart.json"
ORDERS_FILE = "orders.json"

try:
    def load_json(filename, default):
        # Ladda data från en JSON-fil
        # Om filen inte finns eller är trasig, returnera tom lista
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    def save_json(filename, data):
        # Spara data till en JSON-fil
        # Om filen inte finns, skapa den
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"JSON Error: {e}")

class ProductMain:
    def __init__(self, name, description, image, price):
        self.name = name
        self.description = description
        self.image = image
        self.price = price

class Product(ProductMain):
    """
    Skapa produkterna och visa upp dom
    """
    try:
        def __init__(self, name, description, image, price):
            super().__init__(name, description, image, price)

        def visa_produkter(self):
            print(f"Name: {self.name}")
            print(f"Description: {self.description}")
            print(f"Image: {self.image}")
            print(f"Price: ${self.price}")
            print("-" * 40)

        def to_dict(self):
            # Konvertera produkten till en dictionary
            return {
                "name": self.name,
                "description": self.description,
                "image": self.image,
                "price": self.price,
            }

        def from_dict(d):
            return Product(
                name=d["name"],
                description=d["description"],
                image=d["image"],
                price=d["price"],
            )
    except Exception as e:
        print(f"Product Search error: {e}")

class ShoppingCart:
    """
    Lägger till produkter i kundvagn och kan ta bort dem, samt spara/ladda från fil
    """
    try:
        def __init__(self):
            # Skapar en tom lista för att lagra produkter
            self.items = []

        def add(self, product):
            # Lägger till produkten i kundvagnen
            self.items.append(product)
            print(f"Added '{product.name}' to cart.")

        def remove(self, index):
            # Ta bort produkten från kundvagnen med hjälp av index
            # Om index är giltigt, ta bort produkten och skriv ut ett meddelande
            if 0 <= index < len(self.items):
                removed = self.items.pop(index)
                print(f"Removed '{removed.name}' from cart.")
            else:
                print("Invalid item number.")

        def show(self):
            # Om det inte finns några produkter i kundvagnen, skrivs ett errormeddelande ut
            if not self.items:
                print("Cart is empty.")
            else:
                print("\n--- Shopping Cart ---")
                # Loopa igenom alla produkter i kundvagnen och skriv ut namn och pris
                # Skriver ut varje produkt med ett nummer framför
                for i, item in enumerate(self.items, 1):
                    print(f"{i}. {item.name} - ${item.price}")
                print("---------------------\n")

        def clear(self):
            self.items = []

        def to_dict(self):
            # Konvertera listan av Product-objekt till en lista av dictionaries
            # och returnera den
            return [item.to_dict() for item in self.items]

        def from_dict(self, items_list):
            # Konvertera listan av dictionaries till en lista av Product-objekt
            # och spara den i self.items
            self.items = [Product.from_dict(d) for d in items_list]

        def save(self):
            save_json(CART_FILE, self.to_dict())

        def load(self):
            items_list = load_json(CART_FILE, [])
            self.from_dict(items_list)
    except Exception as e:
        print(f"Shopping Cart Error: {e}")

class OrderHistory:
    """Hantera orderhistorik, spara/ladda från fil"""
    try:
        def __init__(self):
            self.orders = []

        def add_order(self, products):
            # Skapa en ny order som innehåller en lista av produkter (som dictionaries)
            # och den totala summan för ordern.
            order = {
                "order_id": len(self.orders) + 1,  # Unik order-ID
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Sätt dagens datum och tid
                "products": [p.to_dict() for p in products],  # Konvertera varje produkt till en dictionary
                "total": sum(float(p.price) for p in products) # Räkna ut totalpriset för ordern
            }
            self.orders.append(order)  # Lägg till ordern i orderhistoriken
            self.save()                # Spara orderhistoriken till fil

        def show(self):
            # Om det inte finns några ordrar, skriv ut ett meddelande och avsluta funktionen
            if not self.orders:
                print("No orders yet")
                return
            print("\n--- Order History ---")
            # Loopa igenom alla ordrar och skriv ut information om varje order
            for i, order in enumerate(self.orders, 1):
                print(f"Order #{i} ({order['date']}):")
                # Loopa igenom alla produkter i ordern och skriv ut namn och pris
                for p in order["products"]:
                    print(f"  - {p['name']} (${p['price']})")
                # Skriv ut totalpriset för ordern
                print(f"  Total: ${order['total']:.2f}")
                print("-" * 30)
            print("---------------------\n")
            time.sleep(1.5)

        def save(self):
            # Spara orderhistoriken till en JSON-fil
            save_json(ORDERS_FILE, self.orders)

        def load(self):
            # Ladda orderhistoriken från en JSON-fil
            self.orders = load_json(ORDERS_FILE, [])
    except Exception as e:
        print(f"Order History Error: {e}")

def search_products(search_terms):
    """
    Söker efter produkter med hjälp av Best Buy API
    """

    query = '&search='.join(search_terms)
    url = (
        f'https://api.bestbuy.com/v1/products(search={query})?format=json&show=sku,name,shortDescription,image,salePrice&apiKey={API_KEY}'
    )

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
        else:
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

def checkout(cart, order_history):
    try:
        if not cart.items:
            print("Cart is empty, cannot checkout.")
            time.sleep(1.5)
        print("\n--- Checkout ---")
        # Kalkylerar total priset på alla produkter i kundvagnen
        total = sum(float(item.price) for item in cart.items)

        for item in cart.items:
            print(f"{item.name} - ${item.price}")
        
        print(f"Total: ${total:.2f}")

        confirm = input("Confirm purchase? (y/n): ").strip().lower()
        if confirm == "y":
            order_history.add_order(cart.items)
            cart.clear()
            cart.save()
            print("Purchase completed")
        else:
            print("Checkout cancelled")
    except Exception as e:
        print(f"Checkout Error: {e}")

if __name__ == "__main__":
    cart = ShoppingCart()
    cart.load()
    order_history = OrderHistory()
    order_history.load()

    while True:
    # Huvudmeny GUI

        print(f"{Fore.LIGHTWHITE_EX}{'═' * 50}{Fore.RESET}")
        print(f" " * 10 + "🏬 Welcome to WorstBuy! 🏬")
        print(f"{Fore.LIGHTWHITE_EX}{'═' * 50}{Fore.RESET}")
        print(f" [1] 🔍  Search for products")
        print(f" [2] 🛒  View your cart")
        print(f" [3] 🗑️   Remove an item from your cart")
        print(f" [4] 💳  Checkout")
        print(f" [5] 📜  View order history")
        print(f" [6] 🚪  Quit")
        print(f"{Fore.LIGHTWHITE_EX}{'═' * 50}{Fore.RESET}")

        choice = input("What would you like to do? ").strip()
        if choice == "6":
            cart.save()
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
                    # Gör om till int och tar bort 1 för rätt index (enklare)
                    ii = int(choice) - 1
                    # Kolla så att det är en giltigt index
                    # och lägger till produkten i kundvagnen
                    if 0 <= ii < len(products):
                        cart.add(products[ii])
                        cart.save()
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
                cart.save()
            else:
                print("Not a valid number 'back' to go back")
        elif choice == "4":
            checkout(cart, order_history)
        elif choice == "5":
            order_history.show()
        else:
            print("Unknown input")

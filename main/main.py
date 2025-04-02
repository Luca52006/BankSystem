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

def search_products(search_terms):
    query = '&search='.join(search_terms)
    url = (
        f'https://api.bestbuy.com/v1/products(search={query})?format=json&show=sku,name,shortDescription,image,salePrice&apiKey={API_KEY}'
    )

    try:
        response = requests.get(url)

        products = response.json().get("products", [])
        return [
            Product(name=item.get("name"), description=item.get("shortDescription"), image=item.get("image"), price=item.get("salePrice"),)
            for item in products
        ]
    except Exception as e:
        return {f"{e}"}

def display_products(products):
    for product in products:
        product.visa_produkter()





if __name__ == "__main__":
    while True:
       search_terms = input("Search: ").split()
       display_products(search_products(search_terms))
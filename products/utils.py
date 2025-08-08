from faker import Faker
from .models import Product
import random


fake = Faker()

def generate_products(num):
    for _ in range(num):
        SKU = fake.word()
        name = fake.word()
        cart_desc = fake.text()
        short_desc = fake.text()
        long_desc = fake.text()
        price = random.uniform(10, 100)
        stok = fake.random_number(digits=3)
        active = fake.boolean()
        Product.objects.create(SKU=SKU, name=name, cart_desc=cart_desc, short_desc=short_desc, long_desc=long_desc, price=price, stok=stok, active=active)
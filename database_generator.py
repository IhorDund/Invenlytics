import random
from datetime import date, timedelta
from queries import add_product, add_purchase, add_sale

# A curated list of realistic product names for random generation
product_names = [
    "Laptop Dell XPS 13", "Smartphone Samsung Galaxy S23", "Tablet iPad Pro",
    "Headphones Sony WH-1000XM5", "Smartwatch Apple Watch", "Camera Canon EOS R5",
    "Printer HP LaserJet Pro", "External SSD Samsung T7", "Gaming Monitor LG UltraGear",
    "Mechanical Keyboard Corsair K95", "Smart TV LG OLED55", "Bluetooth Speaker JBL Flip 5",
    "Gaming Console PS5", "VR Headset Meta Quest 3", "Graphics Card Nvidia RTX 4090"
]

def generate_ean():
    """Generates a random EAN-13 code."""
    return random.randint(1000000000000, 9999999999999)

def generate_large_database(num_products=100, num_purchases=500, num_sales=500, ):
    """
    Generates a substantial amount of records for products, purchases, sales, in the database.

    :param num_products: Total number of products to generate (default: 100)
    :param num_purchases: Total number of purchase records to generate (default: 500)
    :param num_sales: Total number of sale records to generate (default: 500)
    """

    # Product Generation
    for i in range(1, num_products + 1):
        product_name = f"{random.choice(product_names)} {i}"  # Ensure unique product names
        purchase_price = round(random.uniform(10, 2000), 2)  # Random price between 10 and 2000
        quantity = random.randint(1, 100)  # Random quantity between 1 and 100
        ean = generate_ean()  # Generate a random EAN
        add_product(product_name, quantity, purchase_price, ean)  # Pass EAN to the add_product function

    print(f"Added {num_products} products.")

    # Purchase Record Generation
    for _ in range(num_purchases):
        product_id = random.randint(1, num_products)  # Select a random product
        quantity = random.randint(1, 20)  # Random quantity between 1 and 20
        purchase_price = round(random.uniform(10, 2000), 2)  # Random price between 10 and 2000
        purchase_date = date.today() - timedelta(days=random.randint(1, 365))  # Random date within the last year
        add_purchase(product_id, quantity, purchase_price, purchase_date)

    print(f"Added {num_purchases} purchase records.")

    # Sale Record Generation
    for _ in range(num_sales):
        product_id = random.randint(1, num_products)  # Select a random product
        quantity = random.randint(1, 20)  # Random quantity between 1 and 20
        sale_price = round(random.uniform(20, 3000), 2)  # Random price between 20 and 3000
        sale_date = date.today() - timedelta(days=random.randint(1, 365))  # Random date within the last year
        add_sale(product_id, quantity, sale_price, sale_date)

    print(f"Added {num_sales} sale records.")

    # Return Record Generation
    # for _ in range(num_returns):
    #     product_id = random.randint(1, num_products)  # Select a random product
    #     quantity = random.randint(1, 2)  # Random quantity between 1 and 2
    #     return_price = round(random.uniform(20, 3000), 2)  # Random price between 20 and 3000
    #     return_date = date.today() - timedelta(days=random.randint(1, 365))  # Random date within the last year
    #     return_to_stock = random.choice([True, False])  # Random decision to return to stock
    #     add_return(product_id, quantity, return_price, return_date, return_to_stock)
    #
    # print(f"Added {num_returns} return records.")

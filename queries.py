from models import Product, Purchase, Sale
from database import session
from datetime import date


def add_product(name, quantity, purchase_price, ean=None):
    """
    Adds a new product to the database.

    :param name: Product name
    :param quantity: Quantity of product
    :param purchase_price: Purchase price of the product
    :param ean: (Optional) EAN code of the product
    """
    new_product = Product(name=name, quantity=quantity, purchase_price=purchase_price, ean = ean)
    session.add(new_product)
    session.commit()


def get_product_by_id(product_id):
    """
    Retrieves a product by its ID.

    :param product_id: ID of the product to retrieve
    :return: Product object or None if not found
    """
    return session.query(Product).filter(Product.id == product_id).first()


def get_total_income(start_date='1900-01-01', end_date='9999-12-31'):
    """
    Calculates the total income from sales for a specified date range.

    :param start_date: Start date of the reporting period (default: 1900-01-01)
    :param end_date: End date of the reporting period (default: 9999-12-31)
    :return: Total income for the period
    """
    total_sales = session.query(Sale).filter(Sale.date.between(start_date,end_date)).all()
    return sum(sale.sale_price * sale.quantity for sale in total_sales)


def get_total_expense(start_date='1900-01-01', end_date='9999-12-31'):
    """
    Calculates the total expense from purchases for a specified date range.

    :param start_date: Start date of the reporting period (default: 1900-01-01)
    :param end_date: End date of the reporting period (default: 9999-12-31)
    :return: Total expense for the period
    """
    total_purchase = session.query(Purchase).filter(Purchase.date.between(start_date,end_date)).all()
    return sum(purchase.purchase_price * purchase.quantity for purchase in total_purchase)

def update_product_info(product_id, name=None, purchase_price=None, ean=None):
    """
      Updates the information of an existing product by its ID.

      :param product_id: ID of the product to update
      :param name: (Optional) New name of the product
      :param purchase_price: (Optional) New purchase price of the product
      :param ean: (Optional) New EAN code of the product
      :return: Success or failure message
      """
    product = get_product_by_id(product_id)

    if not product:
        return 'Product not found.'

    if name:
        product.name = name
    if purchase_price:
        product.purchase_price = purchase_price
    if ean:
        product.ean = ean

    session.commit()
    return f"Product information for {product.name} updated."



def add_purchase(product_id, quantity, purchase_price, purchase_date=None):
    """
    Adds a purchase entry and updates the stock quantity of the product.

    :param product_id: ID of the product being purchased
    :param quantity: Quantity being purchased
    :param purchase_price: Price per unit of the product
    :param purchase_date: (Optional) Date of purchase (defaults to today)
    :return: Success or failure message
    """
    product = get_product_by_id(product_id)
    if not product:
        return 'Product not found.'
    if quantity <= 0 or purchase_price <= 0:
        return "Quantity and purchase price must be greater than zero."

    purchase_date = purchase_date or date.today()
    purchase = Purchase(product_id=product_id, quantity=quantity, purchase_price=purchase_price, date=purchase_date)

    product.quantity += quantity
    session.add(purchase)
    session.commit()
    return f"Purchase of {product.name} successfully added. Date: {purchase_date}"


def add_sale(product_id, quantity, sale_price, sale_date=None):
    """
        Adds a sale entry and updates the stock quantity of the product.

        :param product_id: ID of the product being sold
        :param quantity: Quantity being sold
        :param sale_price: Price per unit sold
        :param sale_date: (Optional) Date of sale (defaults to today)
        :return: Success or failure message
        """
    product = get_product_by_id(product_id)

    if quantity <= 0 or sale_price <= 0:
        return "Quantity and purchase price must be greater than zero."
    if not product or product.quantity < quantity:
        return "Not enough product in stock or product not found."

    sale_date = sale_date or date.today()
    sale = Sale(product_id=product_id, quantity=quantity, sale_price=sale_price, date=sale_date)
    product.quantity -= quantity
    session.add(sale)
    session.commit()

    return f"Sale of {product.name} successfully added. Date: {sale_date}"


# def add_return(product_id, quantity, return_price, return_date=None, return_to_stock=True):
#     """
#         Adds a return entry and optionally restores stock quantity.
#
#         :param product_id: ID of the product being returned
#         :param quantity: Quantity being returned
#         :param return_price: Price per unit returned
#         :param return_date: (Optional) Date of return (defaults to today)
#         :param return_to_stock: (Optional) Boolean, whether to add returned items back to stock (defaults to True)
#         :return: Success or failure message
#         """
#     product = get_product_by_id(product_id)
#
#     if not product:
#         return 'Product not found.'
#     if quantity <= 0 or return_price <= 0:
#         return "Quantity and return price must be greater than zero."
#
#     total_sold = session.query(Sale).filter(Sale.product_id == product_id).with_entities(func.sum(Sale.quantity)).scalar() or 0
#     total_returned = session.query(Return).filter(Return.product_id == product_id).with_entities(func.sum(Return.quantity)).scalar() or 0
#
#     if total_sold - total_returned >= quantity:
#         return f"Cannot return more items than were sold. Sold: {total_sold}, returned: {total_returned}"
#
#     return_date = return_date or date.today()
#     return_record = Return(
#         product_id=product_id,
#         quantity=quantity,
#         return_price=return_price,
#         date=return_date,
#         return_to_stock='Yes' if return_to_stock == True else 'No'
#
#     )
#
#     if return_to_stock: product.quantity += quantity
#
#     session.add(return_record)
#     session.commit()
#     return f"Return of {product.name} successfully added. Date: {return_date}"


def get_product_stock():
    """
    Retrieves the list of products in stock and their quantities.

    :return: Dictionary of product names and their quantities
    """
    products = session.query(Product).filter(Product.quantity > 0).all()
    stock = {product.name: product.quantity for product in products}
    return stock



def calculate_inventory_purchase_value():
    """
    Calculates the total value of inventory based on purchase prices.

    :return: Total purchase value of all products in stock
    """
    products = session.query(Product).filter(Product.quantity > 0).all()
    total_value = sum(product.quantity * product.purchase_price for product in products)
    return f"Total purchase value of inventory: {total_value}"


def calculate_profit(start_date='1900-01-01', end_date='9999-01-31'):
    """
    Calculates the total profit by comparing sales revenue to purchase costs.

    :param start_date: Start date of the reporting period (default: 1900-01-01)
    :param end_date: End date of the reporting period (default: 9999-12-31)
    :return: Total profit
    """

    total_income = get_total_income(start_date, end_date)
    total_expense = get_total_expense(start_date, end_date)

    profit = total_income - total_expense

    return f"Total profit: {round(profit, 2)}"


def generate_profit_report(start_date='1900-01-01', end_date='9999-01-31'):
    """
    Generates a profit report for a specified date range.

    :param start_date: Start date of the reporting period (default: 1900-01-01)
    :param end_date: End date of the reporting period (default: 9999-12-31)
    :return: Prints total income, total expense, and net profit for the given period

    Retrieves sales and purchase data for the given date range, calculates total income
    (based on sales) and total expenses (based on purchases), then computes net profit
    as income minus expenses.
    """
    income = get_total_income(start_date, end_date)
    expense = get_total_expense(start_date, end_date)
    profit = income - expense
    print('Raport:' if start_date=='1900-01-01' and end_date=='9999-01-31' else f"Report for the period from {start_date} to {end_date}:")
    print(f"Total income: {income}")
    print(f"Total expenses: {expense}")
    print(f"Net profit: {round(profit, 2)}")

    return round(profit, 2)
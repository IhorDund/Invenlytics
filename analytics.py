from sqlalchemy import func, extract
from models import Sale, Purchase, Product
from sqlalchemy.orm import Session
from database import engine, session
from datetime import date, timedelta


def get_fastest_selling_products_out_of_stock():
    """
    Returns a list of products that sold out, sorted by how quickly they sold out.
    Only products with quantity = 0 are included.
    """
    with Session(engine) as session:
        # Fetch products that are out of stock
        results = session.query(
            Product.id,
            Product.name,
            func.min(Purchase.date).label('first_purchase_date'),
            func.max(Sale.date).label('last_sale_date'),
            func.sum(Purchase.quantity).label('total_purchased'),
            func.sum(Sale.quantity).label('total_sold')
        ).filter(Product.quantity == 0).join(Sale, Sale.product_id == Product.id) \
            .join(Purchase, Purchase.product_id == Product.id) \
            .group_by(Product.id) \
            .all()

        # Calculate days to sell out and prepare final list
        product_sales_data = [
            {
                'product_id': prod.id,
                'product_name': prod.name,
                'days_to_sell_out': (prod.last_sale_date - prod.first_purchase_date).days,
                'total_purchased': prod.total_purchased,
                'total_sold': prod.total_sold
            }
            for prod in results
        ]

    # Sort by the speed of selling out
    product_sales_data.sort(key=lambda x: x['days_to_sell_out'])

    # Output results
    print("Out of stock products sorted by speed of selling out:")
    for product in product_sales_data:
        print(
            f"{product['product_name']} (ID: {product['product_id']}) - Sold out in {product['days_to_sell_out']} days. "
            f"Total Purchased: {product['total_purchased']}, Total Sold: {product['total_sold']}")

    return product_sales_data

def get_most_profitable_product_per_day():
    """
    Returns the product that generates the highest average profit per day.
    Profit is calculated as (total_sales - total_expenses) / days on sale.
    """
    with (Session(engine) as session):
        # Fetch total purchase cost and sales income for each product
        results = session.query(
            Product.id,
            Product.name,
            func.min(Purchase.date).label('first_purchase_date'),
            func.max(Sale.date).label('last_sale_date'),
            func.sum(Purchase.quantity * Purchase.purchase_price).label('total_expense'),
            func.sum(Sale.quantity * Sale.sale_price).label('total_income')
        ).join(Sale, Sale.product_id == Product.id) \
        .join(Purchase, Purchase.product_id == Product.id) \
        .group_by(Product.id) \
        .having(func.max(Sale.date) > func.min(Purchase.date)
                ).all()

        # Calculate profit per day for each product
        product_profit_data = []
        for prod in results:
            days_on_sale = (prod.last_sale_date - prod.first_purchase_date).days
            if days_on_sale > 0:  # To avoid division by zero
                total_profit = prod.total_income - prod.total_expense
                profit_per_day = total_profit / days_on_sale
                product_profit_data.append({
                    'product_id': prod.id,
                    'product_name': prod.name,
                    'total_profit': round(total_profit, 2),
                    'days_on_sale': days_on_sale,
                    'profit_per_day': round(profit_per_day, 2)
                })

        # Find the product with the highest average profit per day
        most_profitable_product = max(product_profit_data, key=lambda x: x['profit_per_day'])

    # Output results
    print(f"Most profitable product per day:")
    print(f"{most_profitable_product['product_name']} (ID: {most_profitable_product['product_id']}) - "
          f"Total Profit: {most_profitable_product['total_profit']}, "
          f"Days on Sale: {most_profitable_product['days_on_sale']}, "
          f"Profit per Day: {most_profitable_product['profit_per_day']}")

    return most_profitable_product



def monthly_sales_and_net_profit(year=2024):
    """
    Shows the sales volume and net profit earned per month for a specified year.

    :param year: Year for which to calculate the monthly sales and net profit
    :return: Prints the total quantity sold and net profit for each month in the specified year
    """
    for month in range(1, 13):
        # Total sold products per month
        sales_quantity = (
            session.query(func.sum(Sale.quantity))
            .filter(extract('year', Sale.date) == year)
            .filter(extract('month', Sale.date) == month)
            .scalar() or 0
        )

        # Total income per month
        total_income = (
            session.query(func.sum(Sale.quantity * Sale.sale_price))
            .filter(extract('year', Sale.date) == year)
            .filter(extract('month', Sale.date) == month)
            .scalar() or 0.0
        )

        # Total expense per month
        total_expense = (
            session.query(func.sum(Purchase.quantity * Purchase.purchase_price))
            .filter(extract('year', Purchase.date) == year)
            .filter(extract('month', Purchase.date) == month)
            .scalar() or 0.0
        )

        # Calculate net profit
        net_profit = total_income - total_expense

        print(f"{date(year, month, 1).strftime('%B %Y')}:")
        print(f"  Total Products Sold: {sales_quantity}")
        print(f"  Net Profit: ${round(net_profit, 2)}")


def predict_restock_dates():
    """
    Predicts restock dates for out-of-stock products based on average daily sales.
    """
    with Session(engine) as session:
        results = session.query(
            Product.id,
            Product.name,
            func.sum(Sale.quantity).label('total_sold'),
            func.count(Sale.id).label('sales_count')
        ).join(Sale, Sale.product_id == Product.id) \
        .filter(Product.quantity == 0) \
        .group_by(Product.id) \
        .having(func.count(Sale.id) > 0) \
        .all()

        restock_dates = []
        for prod in results:
            avg_daily_sales = prod.total_sold / prod.sales_count  # Calculate average daily sales
            days_to_restock = 30  # Set a default value; adjust as needed based on business logic
            estimated_restock_date = date.today() + timedelta(days=days_to_restock // avg_daily_sales if avg_daily_sales > 0 else days_to_restock)

            restock_dates.append({
                'product_id': prod.id,
                'product_name': prod.name,
                'estimated_restock_date': estimated_restock_date
            })

    # Output results
    print("Predicted restock dates for out-of-stock products:")
    for item in restock_dates:
        print(f"{item['product_name']} (ID: {item['product_id']}) - Estimated Restock Date: {item['estimated_restock_date']}")

    return restock_dates
from datetime import date
from queries import (add_product, add_purchase, add_sale, update_product_info, get_product_stock,
                     calculate_profit, calculate_inventory_purchase_value, get_total_income, generate_profit_report)
from analytics import get_fastest_selling_products_out_of_stock, get_most_profitable_product_per_day, \
    monthly_sales_and_net_profit


generate_profit_report()
get_fastest_selling_products_out_of_stock()
get_most_profitable_product_per_day()
monthly_sales_and_net_profit(2024)
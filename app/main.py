import json
import os
import sys

from flask import Flask, render_template, request

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from handle_db_connections import create_conn, read_query


app = Flask(__name__)

connection = create_conn()

sql_query = """
SELECT * FROM product_table;
"""

products = read_query(connection, sql_query)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/products")
def product_grid():

    query = request.args.get('search', '') 
    price_range = request.args.get('price_range', '')
    speed = request.args.get('speed', '') 

    filtered_products = products
    if query:
        filtered_products = [product for product in products if query.lower() in product['title'].lower()]
    
    if price_range:
        min_price, max_price = price_range.split('-')
        filtered_products = [
            product for product in filtered_products
            if float(product['price'].replace('€', '').strip()) >= float(min_price)
            and float(product['price'].replace('€', '').strip()) <= float(max_price)
        ]

    if speed:
        speed = int(speed)
        filtered_products = [
            product for product in filtered_products
            if product['speed'] == speed
        ]

    return render_template(
        'product_grid.html', 
        products=filtered_products,
        search_query=query,
        selected_price_range=price_range,
        selected_speed=speed
    )

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, flash, request
import time
from mongo_queries import *
from redis_queries import *
from utils import *

app = Flask(__name__, template_folder="templates", static_folder="stylesheets")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    mongo_dbs = mongo_client.list_databases()
    return render_template("index.html", mongo_dbs=mongo_dbs)

@app.route("/customer/<int:customer_id>/metrics", methods=["GET", "POST"])
def customer_metrics(customer_id: int):
    if (request.method == "POST"):
        manage_post_form()
    start_date = time.time()
    customers_metrics = get_customers_metrics()
    customer_metrics = get_customer_metrics(customer_id)
    if (customers_metrics == None or customer_metrics == None):
        return render_template("undone.html")
    end_date = time.time()
    execution_time_ms = (end_date - start_date) * 1000
    flash(f"Loading data took {execution_time_ms} milliseconds")
    flash("Clear Redis DB")
    customer_name = get_customer_name_mongo(customer_id)
    customer_metrics_comparaison = get_customer_metrics_comparaison(
            customers_metrics, customer_metrics, customer_name)
    return render_template("customer_metrics.html", customer_id=customer_id,
            customer_metrics_comparaison=customer_metrics_comparaison,
            current_url=f"/customer/{customer_id}/metrics")

@app.route("/customer/<int:customer_id>/orders")
def customer_orders(customer_id: int):
    set_customer_orders_in_redis(customer_id)
    set_customer_sorted_orders_in_redis(customer_id)
    order_ids = get_order_ids_customer(customer_id)
    if (order_ids == None):
        return render_template("undone.html")
    return render_template("customer_orders.html", customer_id=customer_id,
            order_ids=order_ids,
            action=f"/customer/{customer_id}/orders")

@app.route("/customer/<int:customer_id>/orders/1")
def customer_orders_1(customer_id: int):
    order_id_input = [request.args.get("order_id_input")]
    product_names = get_product_names(customer_id, order_id_input)
    if (product_names == None):
        return render_template("undone.html")
    return render_template("customer_products.html",
            product_names=product_names)


@app.route("/customer/<int:customer_id>/orders/2")
def customer_orders_2(customer_id: int):
    date_input = request.args.get("date_input")
    order_ids = get_order_ids_date(customer_id, date_input)
    product_names = get_product_names(customer_id, order_ids)
    if (product_names == None):
        return render_template("undone.html")
    return render_template("customer_products.html",
            product_names=product_names)

@app.route("/customer/<int:customer_id>/orders/3")
def customer_orders_3(customer_id: int):
    quantity_input = request.args.get("quantity_input")
    quantities = get_quantities(customer_id, quantity_input)
    if (quantities == None):
        return render_template("undone.html")
    return render_template("customer_quantities.html",
            quantities=quantities)

@app.route("/metrics", methods=["GET", "POST"])
def display_markets_metrics():
    if (request.method == "POST"):
        manage_post_form()
    start_date = time.time()
    markets_metrics = get_markets_metrics()
    end_date = time.time()
    execution_time_ms = (end_date - start_date) * 1000
    flash(f"Loading data took {execution_time_ms} milliseconds")
    bars = create_bars(markets_metrics)
    return render_template("markets_metrics.html",
            bars=bars)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

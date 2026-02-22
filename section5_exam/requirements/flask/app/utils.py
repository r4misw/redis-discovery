from flask import request, flash
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
from typing import List

#create_bar may not be a good function name
def create_bar(x: list, markets_metrics: dict, metric: str):
    y = [ market_metrics[metric] for market_metrics in markets_metrics ]
    df = pd.DataFrame({'x': x, 'y': y})
    data = [
        go.Bar(
            x=df['x'],
            y=df['y']
        )
    ]
    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

def create_bars(markets_metrics: list):
    x = [ market_metrics["_id"] for market_metrics in markets_metrics ]
    bars = dict()
    bars["Sales Price"] = create_bar(x, markets_metrics, "sales_price")
    bars["Sales Count"] = create_bar(x, markets_metrics, "sales_count")
    bars["Customers Count"] = create_bar(x, markets_metrics, "customers_count")
    bars["Orders Count"] = create_bar(x, markets_metrics, "orders_count")
    return bars

def get_customer_metrics_comparaison(customers_metrics: dict,
        customer_metrics: dict, customer_name: str):
    diff_sales = customer_metrics['sales_price'] - customers_metrics['avg_sales_price']
    diff_sales = f'+{diff_sales}' if diff_sales > 0 else diff_sales
    diff_orders = customer_metrics['orders_count'] - customers_metrics['avg_orders_count']
    diff_orders = f'+{diff_orders}' if diff_orders > 0 else diff_orders
    comparaison = list()
    comparaison.append(f"{customer_name} metrics are :")
    comparaison.append(f"Difference with the average sales price per customer : {diff_sales}")
    comparaison.append(f"Difference with the average orders count per customer : {diff_orders}")
    return comparaison

def convert_float(value: str):
    """
    Convert the string value to float is possible
    """
    ### Insert your code here
    try:
        return float(value)
    except (ValueError, TypeError):
        return value
    ### EndInsert

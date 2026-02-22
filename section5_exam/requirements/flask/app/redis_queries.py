import redis
from mongo_queries import *
from typing import List
from flask import flash, request
from datetime import datetime

redis_client = redis.Redis(
    host="redis",
    port=6379,
    health_check_interval=30,
    # needed to decode redis response to utf-8 because redis returns bytes objects
    encoding="utf-8",
    decode_responses=True
)


### Route /metrics ###

def get_markets_metrics():
  """
  Retrieve markets metrics from Redis if possible else retrieve from MongoDB and set markets metrics in Redis
  Return:
    markets_metrics: list[dict]
      Format of dict:
        {
          '_id': <market_1>,
          'sales_price': <market_1_sales_prices>
          'sales_count': <market_1_sales_counts>,
          'customers_count': <market_1_customers_counts>,
          'orders_count': <market_1_orders_counts>
        }
  """
  markets_metrics = redis_client.json().get("markets:metrics")
  if markets_metrics is None:
    flash("Loading markets_metrics from MongoDB")
    markets_metrics = get_markets_metrics_mongo()
    redis_client.json().set("markets:metrics", '$', markets_metrics)
  else:
    flash("Clear Redis DB")
  return markets_metrics

### END ###

# (1)
def manage_post_form():
    """
    Depending on the action from a POST form, we execute an action
    """
    if (request.form.get('action') == "Clear Redis DB"):
        redis_client.flushdb()


### Route : /customer/<customer_id>/metrics ###

# (2)
def get_customers_metrics():
    """
    Retrieve customers metrics from Redis if possible else retrieve from MongoDB and set customers metrics in Redis
    Return:
        customers_metrics: dict
            Format: {'avg_sales_price': <float>, 'avg_orders_count': <float>} 
    """
    key = "customers:metrics"
    customers_metrics = redis_client.hgetall(key)
    if not customers_metrics:
        flash("Loading customers_metrics from MongoDB")
        customers_metrics = get_customers_metrics_mongo()
        redis_client.hset(key, mapping={
            'avg_sales_price': customers_metrics['avg_sales_price'],
            'avg_orders_count': customers_metrics['avg_orders_count']
        })
    else:
        customers_metrics = {
            'avg_sales_price': float(customers_metrics['avg_sales_price']),
            'avg_orders_count': float(customers_metrics['avg_orders_count'])
        }
        flash("Clear Redis DB")
    return customers_metrics

# (3)
def get_customer_metrics(customer_id: int):
    """
    Retrieve customer metrics from Redis if possible else retrieve from MongoDB and set customer metrics in Redis
    Arg:
        customer_id: int
    Return:
        customer_metrics: dict
            Format: {'sales_price': <float>, 'orders_count': <int>}
    """
    key = f"customer:{customer_id}:metrics"
    customer_metrics = redis_client.json().get(key)
    if customer_metrics is None:
        flash(f"Loading customer:{customer_id}:metrics from MongoDB")
        customer_metrics = get_customer_metrics_mongo(customer_id)
        redis_client.json().set(key, '$', customer_metrics)
    else:
        flash("Clear Redis DB")
    return customer_metrics

### END ###


### Route /customer/<customer_id>/orders ###

# (4)
def set_customer_orders_in_redis(customer_id: int):
    """
    Set customer orders from Redis if the key doesn't exist yet
    Arg:
        customer_id: int
    """
    key = f"customer:{customer_id}:orders"
    if redis_client.json().get(key) is None:
        customer_orders = get_customer_orders_mongo(customer_id)
        redis_client.json().set(key, '$', customer_orders)

# (5)
def set_customer_sorted_orders_in_redis(customer_id: int):
    """
    Retrieve customer orders from Redis.JSON object
    Set customer sorted orders if the key doesn't exist yet
    Arg:
        customer_id: int
    """
    key = f"customer:{customer_id}:sorted_orders"
    if not redis_client.exists(key):
        orders_json = redis_client.json().get(f"customer:{customer_id}:orders")
        if orders_json:
            mapping = {}
            for order in orders_json:
                order_id = order['order_id']
                order_date = order['order_date']
                ts = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S").timestamp()
                mapping[str(order_id)] = ts
            if mapping:
                redis_client.zadd(key, mapping)

# (6)
def get_order_ids_customer(customer_id: int):
    """
    Retrieve order ids of a specific customer
    Arg:
        customer_id: int
    Return:
        list[int]
    """
    key = f"customer:{customer_id}:sorted_orders"
    order_ids = redis_client.zrange(key, 0, -1)
    if not order_ids:
        return None
    return [int(oid) for oid in order_ids]

### END ###


### Route /customer/<customer_id>/orders/1 ###

# (7)
def get_product_names(customer_id: int, order_ids: List[int]):
    """
    Retrieve product names of orders
    Args:
        customer_id: int
        order_ids: list[int]
    Return:
        product_names: dict[list]
            Format: {<order_id>: [<product_name_1>, ..., <product_name_n>]
    """
    key = f"customer:{customer_id}:orders"
    orders_json = redis_client.json().get(key)
    if orders_json is None:
        return None
    product_names = {}
    for oid in order_ids:
        oid_int = int(oid)
        for order in orders_json:
            if order['order_id'] == oid_int:
                names = [p['name'] for p in order['products']]
                product_names[oid_int] = names
                break
    return product_names

### END ###


### Route /customer/<customer_id>/orders/2 ###

# (8)
def get_order_ids_date(customer_id: int, date: str):
    """
    Retrieve the order ids passed after a date
    Args:
        customer_id: int,
        date: str
            Format: %Y-%m-%d
    Return:
        order_ids: list[int]
    """
    key = f"customer:{customer_id}:sorted_orders"
    ts = datetime.strptime(date, "%Y-%m-%d").timestamp()
    order_ids = redis_client.zrangebyscore(key, ts, '+inf')
    return [int(oid) for oid in order_ids]

### END ###


### Route customer/<customer_id>/orders/3 ###

# (9)
def get_quantities(customer_id: int, quantity: int):
    """
    Retrieve orders whose quantity is greater than the parameter "quantity"
    Args:
        customer_id: int,
        quantity: int
    Return:
        quantities: dict
            Format: {<order_id_1>: <quantity_1>, ..., <order_id_n>: <quantity_n>}
    """
    key = f"customer:{customer_id}:orders"
    orders_json = redis_client.json().get(key)
    if orders_json is None:
        return None
    quantity = int(quantity)
    quantities = {}
    for order in orders_json:
        if order['total_quantity'] > quantity:
            quantities[order['order_id']] = order['total_quantity']
    return quantities

### END ###

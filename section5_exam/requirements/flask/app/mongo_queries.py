from pymongo import MongoClient

mongo_client = MongoClient(
        host="mongo",
        port=27017,
        username="admin",
        password="pass"
        )

orders = mongo_client['eval']['order']

def get_customers_metrics_mongo():
    aggregation = [
       {
           "$group": {
               "_id": "$customer.id",
               "avg_sales_price_per_customer": { "$avg": "$sales" },
               "orders" : { "$addToSet": "$id" }
           }
       },
       {
           "$group": {
               "_id": "all",
               "avg_sales_price": { "$avg": "$avg_sales_price_per_customer" },
               "avg_orders_count": { "$avg": { "$size": "$orders" } }
           }
       },
       {
           "$project": {
               "_id": 0,
               "avg_sales_price": 1,
               "avg_orders_count": 1
           }
       }
    ]
    result = list(orders.aggregate(aggregation))
    return result[0]

def get_customer_name_mongo(customer_id: int):
    aggregation = [
        {
            "$match": {
                "customer.id" : customer_id,
                "customer.firstname": { "$exists": True },
                "customer.lastname": { "$exists": True },
            }
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "_id": 0,
                "firstname": "$customer.firstname",
                "lastname": "$customer.lastname",
            }
        }
    ]
    result = list(orders.aggregate(aggregation))
    customer_name = result[0]["firstname"] + ' ' + result[0]["lastname"]
    return customer_name
        

def get_customer_orders_mongo(customer_id: int):
    aggregation = [
        {
            "$match": {
                "customer.id" : customer_id
            }
        },
        {
            "$group": {
                "_id": "$id",
                "products": {
                    "$addToSet": "$product"
                },
                "total_sales": { "$sum": "$sales" },
                "total_quantity": { "$sum": "$quantity" },
                "order_date": { "$first": "$date order" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "order_id": "$_id",
                "products": 1,
                "total_sales": 1,
                "total_quantity": 1,
                "order_date": 1
            }
        }
    ]
    result = list(orders.aggregate(aggregation))
    return result

def get_customer_metrics_mongo(customer_id: int):
    aggregation = [
        {
            "$match": {
                "customer.id" : customer_id
            }
        },
        {
            "$group": {
                "_id": "all",
                "sales_price": { "$sum": "$sales" },
                "orders": { "$addToSet": "$id" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "sales_price": 1,
                "orders_count" : { "$size": "$orders" },
            }
        }
    ]
    result = list(orders.aggregate(aggregation))
    return result[0]

def get_markets_metrics_mongo():
    aggregation = [
        {
            "$group": {
                "_id": "$market",
                "sales_price": { "$sum": "$sales" },
                "sales_count": { "$sum": "$quantity" },
                "customers" : { "$addToSet": "$customer.id" },
                "orders" : { "$addToSet": "$id" }
            }
        },
        {
            "$project": {
                "_id": 1,
                "sales_price": 1,
                "sales_count": 1,
                "customers_count": { "$size": "$customers" },
                "orders_count": { "$size": "$orders" }
            }
        }
    ]
    result = list(orders.aggregate(aggregation))
    return result

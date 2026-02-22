import redis


if __name__ == "__main__":
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True, health_check_interval=30)

    r.set("book:1", "Good Omens", ex=5)
    print("book:1 ttl:", r.ttl("book:1"))

    r.delete("movies")
    r.rpush("movies", "Titanic", "Terminator", "Jaws", "Shrek", "Psycho", "City of God")
    print("movies:", r.lrange("movies", 0, -1))

    r.hset("car_dealer:1", mapping={"brand": "Mercedes", "model": "Classe a", "year": 2009})
    result = r.hmget("car_dealer:1", ["brand", "model"])
    print("car_dealer:1 brand/model:", result)

    data = [{
        "name": "Paris",
        "country": "France",
        "monuments": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
        ],
        "population": 2206488,
        "cityCode": "PAR",
        "languagesSpoken": [
            "French",
            "English",
            "Spanish",
        ],
        "areaSquareKm": 105.4,
        "timezone": "Central European Time (CET)",
    }]
    r.delete("city:1")
    r.json().set("city:1", "$", data)
    data_name = r.json().get("city:1", "$..name")
    print("city:1 name:", data_name)

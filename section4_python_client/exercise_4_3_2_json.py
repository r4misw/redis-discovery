import json

import redis
from cerberus import Validator


schema = {
    "name": {"required": True, "type": "string"},
    "country": {"required": True, "type": "string"},
    "monuments": {"required": True, "type": "list"},
    "population": {"required": True, "type": "integer"},
    "cityCode": {"required": True, "type": "string"},
    "languagesSpoken": {"required": True, "type": "list"},
    "areaSquareKm": {"required": True, "type": "float"},
    "timezone": {"required": True, "type": "string"},
}


if __name__ == "__main__":
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True, health_check_interval=30)

    with open("data/cities.json", encoding="utf-8") as input_file:
        cities = json.load(input_file)

    v = Validator(schema)
    cities_filtered = list(filter(lambda x: v.validate(x), cities))
    print("cities count:", len(cities))
    print("cities filtered count:", len(cities_filtered))

    r.json().set("json_cities", "$", cities_filtered)

    data_name = r.json().get("json_cities", "$..name")
    r.delete("list_cities")
    r.rpush("list_cities", *data_name)

    names = r.json().get("json_cities", "$..name")
    populations = r.json().get("json_cities", "$..population")
    area_square_kms = r.json().get("json_cities", "$..areaSquareKm")
    for name, pop, area in zip(names, populations, area_square_kms):
        print(f"{name} has {pop} people in {area} square km")

    big_cities = r.json().get("json_cities", "$.[?(@.population>5000000)].name")
    print(f"Les villes les plus peuplées sont {', '.join(big_cities)}")

    big_cities_2 = r.json().get("json_cities", "$.[?(@.population>5000000&&@.areaSquareKm<1000)].name")
    print(f"Les villes >5M et <1000km² sont {', '.join(big_cities_2)}")

    names = r.json().get("json_cities", "$..name")
    populations = r.json().get("json_cities", "$..population")
    area_square_kms = r.json().get("json_cities", "$..areaSquareKm")

    for key in r.scan_iter("city:*"):
        r.delete(key)

    for id_, (name, pop, area) in enumerate(zip(names, populations, area_square_kms)):
        r.hset(f"city:{id_}", mapping={"name": name, "pop": pop, "area": area})

    print("hash city:0:", r.hgetall("city:0"))

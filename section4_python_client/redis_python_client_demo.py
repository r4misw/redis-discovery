import json
from pathlib import Path

import redis


def compact_json_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    return "".join(content.split())


def main() -> None:
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    print("PING:", client.ping())

    client.hset("user:python:1", mapping={"firstname": "Nicolas", "lastname": "Cage", "age": 59, "job": "actor"})
    firstname, lastname = client.hmget("user:python:1", ["firstname", "lastname"])
    print("HASH user:python:1 firstname/lastname:", firstname, lastname)

    client.execute_command("JSON.SET", "starwars:people:python", "$", '{"name":"Luke Skywalker"}')
    client.execute_command("JSON.SET", "starwars:people:python", "mass", 77)
    mass_type = client.execute_command("JSON.TYPE", "starwars:people:python", "mass")
    mass_after = client.execute_command("JSON.NUMINCRBY", "starwars:people:python", "mass", 10)
    print("JSON mass type:", mass_type)
    print("JSON mass after +10:", mass_after)

    client.execute_command("JSON.SET", "starwars:people:python", "scores", "[]")
    client.execute_command("JSON.ARRAPPEND", "starwars:people:python", "scores", 85, 90, 75, 92, 95, 83)
    client.execute_command("JSON.ARRTRIM", "starwars:people:python", "scores", 1, -2)
    idx_75 = client.execute_command("JSON.ARRINDEX", "starwars:people:python", "scores", 75)
    idx_80 = client.execute_command("JSON.ARRINDEX", "starwars:people:python", "scores", 80)
    print("JSON ARRINDEX 75:", idx_75)
    print("JSON ARRINDEX 80:", idx_80)

    food_path = Path("/home/ubuntu/food.json")
    compact = compact_json_file(food_path)
    client.execute_command("JSON.SET", "supermarket:python", "$", compact)

    vegetables = client.execute_command("JSON.GET", "supermarket:python", "$.food.vegetables.*")
    candy_ids = client.execute_command("JSON.GET", "supermarket:python", "$.food.candies.*.id")
    prices = client.execute_command("JSON.GET", "supermarket:python", "$..price")
    fruit_colors = client.execute_command("JSON.GET", "supermarket:python", "$.food.fruits[1].colors")
    fruits_price_range = client.execute_command(
        "JSON.GET",
        "supermarket:python",
        "$.food.fruits[?(@.price>1&&@.price<1.5)].name",
    )

    print("Vegetables:", json.loads(vegetables))
    print("Candy IDs:", json.loads(candy_ids))
    print("Prices:", json.loads(prices))
    print("2nd fruit colors:", json.loads(fruit_colors))
    print("Fruits price in (1,1.5):", json.loads(fruits_price_range))


if __name__ == "__main__":
    main()
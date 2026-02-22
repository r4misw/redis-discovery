import json
import random

import redis


if __name__ == "__main__":
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True, health_check_interval=30)

    players = {}
    r.delete("players")

    with open("data/teams.json", encoding="utf-8") as input_file:
        teams = json.load(input_file)
        for team in teams:
            team_name = list(team.keys())[0]
            for player_name, score in team[team_name].items():
                players[f"{team_name}-{player_name}"] = score

    r.zadd("players", players)
    print("zscan players:", r.zscan("players"))

    print("top 10:", r.zrange("players", 0, 9, desc=True, withscores=True))

    r.zremrangebyrank("players", 0, 19)
    removed_lt_100 = r.zremrangebyscore("players", "-inf", 100)
    print("removed score < 100:", removed_lt_100)

    print("Banana_Friendly remaining:", r.zscan("players", match="Banana_Friendly*"))

    current_players = r.zscan("players")
    new_players = {}

    random.seed(42)
    for member, _score in current_players[1]:
        new_players[member] = random.randint(100, 200)

    improved = r.zadd("players", new_players, ch=True, gt=True)
    print("players improved:", improved)

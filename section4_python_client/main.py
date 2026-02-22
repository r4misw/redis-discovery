import os

import redis


if __name__ == "__main__":
    redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True, health_check_interval=30)
    print(r.ping())

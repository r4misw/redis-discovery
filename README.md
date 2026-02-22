# Redis Discovery

Travail complet de découverte de Redis : configuration, module JSON, client Python et évaluation finale avec Flask + MongoDB.

## Structure

```
redis-discovery/
├── section3_config_json/     # Configuration Redis & module RedisJSON
│   ├── conf/redis_7.2.conf   # Config personnalisée (mémoire, snapshots, logs)
│   └── modules/librejson.so  # Module RedisJSON
│
├── section4_python_client/   # Exercices Python avec redis-py
│   ├── main.py               # Test connexion Redis
│   ├── exercise_4_2_basic.py # Opérations basiques (Strings, Hashes, Lists)
│   ├── exercise_4_3_1_sorted_set.py  # Sorted Sets (équipes sportives)
│   ├── exercise_4_3_2_json.py        # RedisJSON (villes)
│   ├── run_all.py            # Lanceur de tous les scripts
│   └── data/                 # Datasets JSON
│
└── section5_exam/            # Évaluation : API Flask + Redis cache + MongoDB
    ├── docker-compose.yml    # 3 services : Redis, MongoDB, Flask
    └── requirements/
        ├── flask/app/
        │   ├── redis_queries.py   # 9 fonctions Redis (cache)
        │   ├── mongo_queries.py   # Requêtes MongoDB (agrégations)
        │   ├── main.py            # Routes Flask
        │   └── utils.py           # Utilitaires (graphiques, comparaisons)
        ├── redis/conf/            # Config Redis
        ├── redis/modules/         # Module RedisJSON
        └── mongo/init/            # Script d'import des données
```

## Stack technique

- **Redis** 7.2.0 + RedisJSON
- **MongoDB** 5.0
- **Flask** (Python 3.8)
- **Docker Compose**

## Lancement de l'évaluation

```bash
cd section5_exam
docker compose up --build -d
# API accessible sur http://localhost:5000
```


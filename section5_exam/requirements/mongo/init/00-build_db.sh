#!/bin/bash

env_vars=(
    "MONGO_INITDB_ROOT_USERNAME"
  "MONGO_INITDB_ROOT_PASSWORD"
  "MONGO_INITDB_DATABASE"
)

function is_env_var {
  # Check if the environment variable are set
  # If not, the service mongo stop
    echo "Checking environment variable"
    for env_var in ${env_vars[@]}
    do
        if [[ -z "${!env_var:-}" ]]; then
            echo "$env_var is not present, please add it on the docker-compose.yml file"
            exit 1
        fi
        echo "$env_var set"
    done
    echo "Checking completed"
}

function build_user_db_collection {
  # Import the file orders.json into the collection order in the eval database
    mongoimport --authenticationDatabase admin --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --db $MONGO_INITDB_DATABASE --collection order --jsonArray --type json --file data/json/orders.json
}

function main {
  # execute the two functions above
    is_env_var
    build_user_db_collection
}

main

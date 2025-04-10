#!/bin/bash

set -e
set -u

function create_user_and_database() {
    local database=$1
    echo "Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER $database WITH ENCRYPTED PASSWORD '$database';
        CREATE DATABASE $database WITH OWNER $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

function create_tables_in_main() { #user_service
    local database=$1
    echo "Creating tables in database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$database" <<-EOSQL
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            nickname VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            phone_number VARCHAR(20),
            name VARCHAR(100),
            surname VARCHAR(100),
            birth_date DATE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            token VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP
        );

        -- Назначение прав пользователю
        GRANT ALL PRIVILEGES ON TABLE users TO $database;
        GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO $database;
        GRANT ALL PRIVILEGES ON TABLE tokens TO $database;
EOSQL
}

function create_tables_in_posts() { #posts_service
    local database=$1
    echo "Creating tables in database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$database" <<-EOSQL
        CREATE TABLE posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            creator_id INT NOT NULL,
            private BOOLEAN DEFAULT FALSE,
            tags TEXT[] DEFAULT ARRAY[]::TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE comments (
            id SERIAL PRIMARY KEY,
            post_id INT REFERENCES posts(id),
            user_id INT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE likes (
            id SERIAL PRIMARY KEY,
            post_id INT REFERENCES posts(id),
            user_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Назначение прав пользователю
        GRANT ALL PRIVILEGES ON TABLE posts TO $database;
        GRANT ALL PRIVILEGES ON TABLE comments TO $database;
        GRANT ALL PRIVILEGES ON TABLE likes TO $database;
        GRANT USAGE, SELECT ON SEQUENCE posts_id_seq TO $database;
        GRANT USAGE, SELECT ON SEQUENCE comments_id_seq TO $database;
        GRANT USAGE, SELECT ON SEQUENCE likes_id_seq TO $database;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_user_and_database $db

        if [ "$db" = "main" ]; then
            create_tables_in_main $db
        elif [ "$db" = "posts" ]; then
            create_tables_in_posts $db
        fi
    done
    echo "Multiple databases and tables created"
fi
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database=os.getenv('database'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    host=os.getenv('host'),
    port=os.getenv('port')
)

cur = conn.cursor()

create_users_table = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    login_try_count INT NOT NULL 
);
"""

create_todos_table = """CREATE TABLE IF NOT EXISTS todos(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    todo_type VARCHAR(15) NOT NULL,
    user_id INT REFERENCES users(id)
);
"""


def create_table():
    cur.execute(create_users_table)
    cur.execute(create_todos_table)
    conn.commit()


def migrate():
    insert_into_users = """
    INSERT INTO users (username, password, role, status,login_try_count) 
    VALUES ('Admin','admin123','SUPERADMIN','ACTIVE',0);
    """
    cur.execute(insert_into_users)
    conn.commit()


def init():
    create_table()
    migrate()


if __name__ == '__main__':
    init()

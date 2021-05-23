import sqlite3


# Створення бази даних
def init_db():
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'user'(user_id VARCHAR(32) PRIMARY KEY ,
     user_group VARCHAR(8), course VARCHAR(8), week SMALLINT,
     first_name VARCHAR(32), last_name VARCHAR(32), email VARCHAR(32) , username VARCHAR(32)) """)
    conn.commit()


# додавання користувача
def add_user(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"insert into 'user'(user_id, first_name, last_name, username) values ({user[0]},"
                   f" '{user[1]}', '{user[2]}', '{user[3]}')")
    conn.commit()


# додавання курсу користувача
def add_course(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET course = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


# додавання групи користувача
def add_group(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET user_group = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


# додавання тиждня користувача
def add_week(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET week = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


# додавання тиждня користувача
def add_firstName(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET first_name = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


def add_lastName(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET last_name = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


def add_email(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE  'user' SET email = '{user[1]}' WHERE user_id = {user[0]}")
    conn.commit()


# отримання рокладу користувача
def get_schedule(user):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id, course, user_group, week FROM 'user' WHERE user_id = {user}")
    user_data = cursor.fetchone()
    conn.commit()
    return user_data


# отримання усіх користувачів
def get_all():
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id, course, user_group, week FROM 'user'")
    user_data = cursor.fetchall()
    conn.commit()
    return user_data


def get_user_group(user_id):
    data = get_schedule(user_id)
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT first_name, last_name, email, username FROM 'user' "
                   f"WHERE user_group='{data[2]}' and course='{data[1]}'")
    user_data = cursor.fetchall()
    conn.commit()
    return user_data


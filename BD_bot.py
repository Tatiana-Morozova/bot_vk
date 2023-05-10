from secret import db_url_object
import psycopg2


conn = psycopg2.connect(
    user='postgres',
    password='    ',
    database='user_V'
)

conn.autocommit = True
# схема БД

def create_db():
    with conn.cursor() as cur:
        # Функция, создающая структуру БД. Т.е. в данной функции создаются таблицы в базе данных

        cur.execute("""create table IF NOT exists users (
                        profile_id int,
                        worksheet_id int);
                        """)
        conn.commit()
        cur.execute(""" SELECT worksheet_id FROM users;""")


create_db()

def add_users(user_id):
    with conn.cursor() as cur:  # Функция, позволяющая добавить нового пользователя
        cur.execute(f"""insert into users(profile_id) values({user_id});""")
        conn.commit()
        cur.execute(""" SELECT profile_id FROM users;""")

def add_user_viewed(id_vk):
    with conn.cursor() as cur:
        cur.execute(f"""insert into users(worksheet_id) values({id_vk});""")
        conn.commit()
        cur.execute(""" SELECT worksheet_id FROM users;""")


def drop_table():
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE users;""")
        conn.commit()









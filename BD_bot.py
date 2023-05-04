from secret import db_url_object
import psycopg2
from main import *

conn = psycopg2.connect(
    user='postgres',
    password='    ',
    database='user_V'
)

conn.autocommit = True
# схема БД
#with psycopg2.connect(database='user_V', user='postgres', password='    ') as conn:
def create_db():
    with conn.cursor() as cur:
        # Функция, создающая структуру БД. Т.е. в данной функции создаются таблицы в базе данных
        cur.execute("""create table IF NOT exists users (
                        profile_id int not null primary key unique);
                        """)

        cur.execute("""create table IF NOT exists user_viewed (
                        worksheet_id int not null primary key unique,
                        profile_id int not null references users(profile_id));
                        """)
        conn.commit()
        cur.execute(""" SELECT worksheet_id FROM user_viewed;""")
        print(cur.fetchall())
        print('BD создана')

create_db()

def add_users(user_id):
 with conn.cursor() as cur:  # Функция, позволяющая добавить нового пользователя
    cur.execute(f"""insert into users(profile_id) values({user_id});""")
    conn.commit()
    cur.execute(""" SELECT profile_id FROM users;""")
    print(cur.fetchall())

def add_user_viewed(id_vk):
    with conn.cursor() as cur:
        cur.execute(f"""insert into user_viewed(worksheet_id) values({id_vk});""")
        conn.commit()
        cur.execute(""" SELECT worksheet_id FROM user_viewed;""")
        print(cur.fetchall())
         #if not user_id in res_user_viewed:  # ищем ID в запросе с таблицы, если нет добавляеем его айди
             #add_user_viewed(user['id'])












import psycopg2
from pprint import pprint


db_name = 'client_db_netology'
db_user = ''
db_password = ''


def create_bd():
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE client_phone;
                """)

        cur.execute("""
                DROP TABLE client_info;
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS client_info(
                    user_id int NOT NULL UNIQUE,
                    user_first_name VARCHAR(40) NOT NULL,
                    user_last_name VARCHAR(40) NOT NULL,
                    user_email VARCHAR(80) NOT NULL UNIQUE
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS client_phone(
                    id SERIAL PRIMARY KEY,
                    user_id int REFERENCES client_info(user_id),
                    user_phone_number TEXT
                );
                """)
        conn.commit()
    conn.close()


def add_client(user_id, first_name, last_name, email, phone_number=None):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client_info(user_id, user_first_name, user_last_name, user_email) VALUES(%s, %s, %s, %s);
                """, (user_id, first_name, last_name, email,))

        cur.execute("""
                INSERT INTO client_phone(user_id, user_phone_number) VALUES(%s, %s);
                """, (user_id, phone_number,))
        conn.commit()
    conn.close()


def add_phone_number(user_id, phone_number):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client_phone(user_id, user_phone_number) VALUES(%s, %s); 
                """, (user_id, phone_number,))
        conn.commit()
    conn.close()


def update_client_info(user_id, first_name=None, last_name=None, email=None, phone_number=None, old_phone_number=None):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE client_phone 
                SET 
                user_phone_number = %s 
                WHERE 
                user_phone_number = %s; 
                """, (phone_number, old_phone_number,))

        cur.execute("""
                UPDATE client_info 
                SET 
                user_first_name = %s,
                user_last_name = %s,
                user_email = %s
                WHERE
                user_id = %s
                """, (first_name, last_name, email, user_id,))
        conn.commit()
    conn.close()


def delete_phone(user_id, phone_number):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client_phone WHERE user_id = %s AND user_phone_number = %s; 
                """, (user_id, phone_number,))
        conn.commit()
    conn.close()


def delete_client(user_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client_phone WHERE user_id = %s;
                DELETE FROM client_info WHERE user_id = %s;
                """, (user_id, user_id,))
        conn.commit()
    conn.close()


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    with conn.cursor() as cur:
        cur.execute("""
                SELECT user_first_name, user_last_name, user_email, user_phone_number FROM client_info ci
                LEFT JOIN client_phone cp ON ci.user_id = cp.user_id
                WHERE user_first_name = %s OR user_last_name = %s OR user_email = %s OR user_phone_number = %s;
                """, (first_name, last_name, email, phone_number,))
        pprint(cur.fetchall())
    conn.close()


if __name__ == '__main__':
    # create_bd()
    # add_client()
    # add_phone_number(2, '7')
    # update_client_info()
    # delete_phone()
    # delete_client()
    # find_client()

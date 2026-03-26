# connect.py
import psycopg2
from config import config

def get_connection():
    """
    Создает и возвращает соединение с базой данных PostgreSQL
    """
    try:
        params = config()  # берём параметры из config.py
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка подключения к базе:", error)
        return None
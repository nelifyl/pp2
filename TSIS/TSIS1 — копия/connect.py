import psycopg2
from config import load_config

def connect():
    config = load_config()
    conn = psycopg2.connect(**config)
    return conn
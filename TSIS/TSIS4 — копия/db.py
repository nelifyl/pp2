import psycopg2
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="snake_game",
            user="postgres",
            password="12345678",  # Измените на ваш пароль
            port="5432"
        )
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.conn.commit()
        cursor.close()
    
    def get_or_create_player(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            player_id = result[0]
        else:
            cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
            player_id = cursor.fetchone()[0]
            self.conn.commit()
        
        cursor.close()
        return player_id
    
    def save_game_result(self, username, score, level_reached):
        player_id = self.get_or_create_player(username)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level_reached)
        )
        self.conn.commit()
        cursor.close()
    
    def get_top_scores(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC
            LIMIT %s
        """, (limit,))
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def get_personal_best(self, username):
        player_id = self.get_or_create_player(username)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT MAX(score) FROM game_sessions WHERE player_id = %s
        """, (player_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result if result else 0
    
    def close(self):
        self.conn.close()
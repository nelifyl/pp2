import json
import os
import sqlite3

SETTINGS_FILE = "settings.json"
DB_FILE = "racer.db"

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            coins INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_score(name, score, distance, coins):
    """Сохранение результата в БД"""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO scores (name, score, distance, coins)
        VALUES (?, ?, ?, ?)
    ''', (name, score, distance, coins))
    
    conn.commit()
    conn.close()

def get_all_scores(limit=50):
    """Получение всех результатов из БД (сортировка по score DESC)"""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, score, distance, coins, date 
        FROM scores 
        ORDER BY score DESC 
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{"name": row[0], "score": row[1], "distance": row[2], "coins": row[3], "date": row[4]} for row in rows]

def get_top_scores(limit=10):
    """Получение топ результатов"""
    return get_all_scores(limit)[:limit]

def get_player_best(name):
    """Получение лучшего результата игрока"""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT MAX(score) FROM scores WHERE name = ?
    ''', (name,))
    
    result = cursor.fetchone()[0]
    conn.close()
    
    return result if result else 0

def get_total_players():
    """Получение количества уникальных игроков"""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(DISTINCT name) FROM scores')
    count = cursor.fetchone()[0]
    conn.close()
    
    return count

def load_settings():
    """Загрузка настроек"""
    if not os.path.exists(SETTINGS_FILE):
        save_settings({"sound": True, "difficulty": "normal", "car_color": "green"})
    return json.load(open(SETTINGS_FILE))

def save_settings(data):
    """Сохранение настроек"""
    json.dump(data, open(SETTINGS_FILE, "w"))

# Для обратной совместимости со старым кодом
def load_scores():
    """Загрузка из JSON (для совместимости)"""
    return get_top_scores()
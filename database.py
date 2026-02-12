"""
SWILL DATABASE - SQLITE ВЕРСИЯ
ДЛЯ БОЛЬШИХ НАГРУЗОК
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'swill_adult.db'

def init_sqlite_db():
    """ИНИЦИАЛИЗАЦИЯ SQLITE БАЗЫ"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ТАБЛИЦА ВИДЕО
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            thumbnail TEXT,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ТАБЛИЦА ДОХОДОВ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS earnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            amount REAL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos (id)
        )
    ''')
    
    # ТАБЛИЦА НАСТРОЕК
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # ПРОВЕРЯЕМ ЕСТЬ ЛИ АДМИН
    cursor.execute("SELECT * FROM settings WHERE key = 'admin_password'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO settings (key, value) VALUES (?, ?)", 
                      ('admin_password', 'swillmaster2025'))
    
    # ДОБАВЛЯЕМ ТЕСТОВЫЕ ВИДЕО
    cursor.execute("SELECT COUNT(*) FROM videos")
    if cursor.fetchone()[0] == 0:
        test_videos = [
            ('🔥 SWILL PREMIUM 4K', 'Эксклюзивный контент', 'sample1.mp4', 'thumb1.jpg', 15420),
            ('💎 SWILL GOLD', 'Видео недели', 'sample2.mp4', 'thumb2.jpg', 8930),
            ('⭐ SWILL VIP', 'Только для подписчиков', 'sample3.mp4', 'thumb3.jpg', 12750)
        ]
        cursor.executemany(
            "INSERT INTO videos (title, description, filename, thumbnail, views) VALUES (?, ?, ?, ?, ?)",
            test_videos
        )
    
    conn.commit()
    conn.close()
    print("✅ SQLite база данных инициализирована")

def get_sqlite_db():
    """ПОЛУЧИТЬ СОЕДИНЕНИЕ"""
    return sqlite3.connect(DB_PATH)

if __name__ == '__main__':
    init_sqlite_db()
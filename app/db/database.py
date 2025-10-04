"""
Khan AI - Database Management
"""
import aiosqlite
from pathlib import Path
from datetime import datetime

DB_PATH = Path("khan.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quirks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quirk TEXT NOT NULL,
                peso REAL DEFAULT 1.0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction TEXT,
                feedback INTEGER,
                sarcasmo_score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                decaimiento REAL DEFAULT 1.0
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS voice_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_path TEXT,
                transcript TEXT,
                confidence REAL,
                language TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()

async def add_quirk(quirk: str, peso: float = 1.0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO quirks (quirk, peso) VALUES (?, ?)",
            (quirk, peso)
        )
        await db.commit()

async def get_quirks(limit: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT quirk, peso FROM quirks ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def add_log(interaction: str, feedback: int = 0, sarcasmo_score: int = 0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (interaction, feedback, sarcasmo_score) VALUES (?, ?, ?)",
            (interaction, feedback, sarcasmo_score)
        )
        await db.commit()

async def get_recent_logs(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT interaction, feedback, sarcasmo_score, timestamp FROM logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def set_user_memory(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM user_memory WHERE key = ?",
            (key,)
        )
        await db.execute(
            "INSERT INTO user_memory (key, value) VALUES (?, ?)",
            (key, value)
        )
        await db.commit()

async def get_user_memory(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT value FROM user_memory WHERE key = ? ORDER BY timestamp DESC LIMIT 1",
            (key,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def cleanup_old_quirks():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM quirks WHERE id NOT IN (
                SELECT id FROM quirks ORDER BY timestamp DESC LIMIT 5
            )
        """)
        await db.commit()

async def apply_decay():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE logs 
            SET decaimiento = decaimiento * 0.8 
            WHERE julianday('now') - julianday(timestamp) > 7
        """)
        await db.commit()

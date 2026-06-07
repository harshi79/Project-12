"""
ALYA - Professional Database Layer
SQLite with export/import support for Render restarts
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DB_PATH = "alya_bot.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            plan TEXT DEFAULT 'free',
            plan_expiry INTEGER DEFAULT 0,
            daily_limit INTEGER DEFAULT 30,
            daily_count INTEGER DEFAULT 0,
            daily_date TEXT,
            generations_made INTEGER DEFAULT 0,
            chat_history TEXT DEFAULT '[]',
            safety_mode INTEGER DEFAULT 1,
            steps INTEGER DEFAULT 5,
            dimensions TEXT DEFAULT '1:1',
            art_style TEXT DEFAULT 'none',
            last_msg_time INTEGER DEFAULT 0,
            first_seen TEXT,
            language TEXT DEFAULT 'hinglish',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Plans backup (for quick lookup)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            user_id INTEGER PRIMARY KEY,
            plan TEXT,
            limit_val INTEGER,
            expiry INTEGER
        )
    """)
    
    # Media (pics & stickers)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,  -- 'pic' or 'sticker'
            file_id TEXT UNIQUE
        )
    """)
    
    # Force join channels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id TEXT PRIMARY KEY,
            link TEXT,
            name TEXT
        )
    """)
    
    # Blocked users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked (
            user_id TEXT PRIMARY KEY
        )
    """)
    
    # Broadcast state (temporary)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS broadcast_state (
            user_id INTEGER PRIMARY KEY,
            waiting INTEGER DEFAULT 0,
            type TEXT,
            content TEXT,
            caption TEXT
        )
    """)
    
    # Mood
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood (
            key TEXT PRIMARY KEY,
            value TEXT,
            changed_at INTEGER
        )
    """)
    
    # Payments tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            stars INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Analytics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            date TEXT PRIMARY KEY,
            messages INTEGER DEFAULT 0,
            images INTEGER DEFAULT 0,
            new_users INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# ==================== USER FUNCTIONS ====================

def get_user(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_or_update_user(user_id: int, username: str = None, first_name: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("""
        INSERT INTO users (user_id, username, first_name, first_seen, daily_date)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = COALESCE(excluded.username, username),
            first_name = COALESCE(excluded.first_name, first_name)
    """, (user_id, username, first_name, today, today))
    
    conn.commit()
    conn.close()

def update_user_plan(user_id: int, plan: str, days: int = 0):
    conn = get_connection()
    cursor = conn.cursor()
    
    expiry = 0
    if days > 0:
        expiry = int((datetime.now() + timedelta(days=days)).timestamp())
    
    limit_val = {"free": 30, "weekly": 200, "monthly": 600, "yearly": 1200}.get(plan, 30)
    
    cursor.execute("""
        UPDATE users SET 
            plan = ?, 
            plan_expiry = ?, 
            daily_limit = ?
        WHERE user_id = ?
    """, (plan, expiry, limit_val, user_id))
    
    conn.commit()
    conn.close()

def get_user_plan(user_id: int) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plan, plan_expiry, daily_limit, daily_count, daily_date FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"plan": "free", "limit": 30, "expiry": 0, "count": 0}
    
    plan, expiry, limit_val, count, daily_date = row
    
    # Check expiry
    if plan != "free" and expiry > 0 and datetime.now().timestamp() > expiry:
        plan = "free"
        limit_val = 30
        expiry = 0
        update_user_plan(user_id, "free")
    
    today = datetime.now().strftime("%Y-%m-%d")
    if daily_date != today:
        count = 0
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET daily_count = 0, daily_date = ? WHERE user_id = ?", (today, user_id))
        conn.commit()
        conn.close()
    
    return {
        "plan": plan,
        "limit": limit_val,
        "expiry": expiry,
        "count": count or 0
    }

def increment_daily_count(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET daily_count = daily_count + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user_setting(user_id: int, key: str, value):
    conn = get_connection()
    cursor = conn.cursor()
    if key in ["safety_mode", "steps", "dimensions", "art_style", "chat_history", "language"]:
        cursor.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def get_user_settings(user_id: int) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT safety_mode, steps, dimensions, art_style, generations_made, chat_history, language
        FROM users WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {
            "safety_mode": True,
            "steps": 5,
            "dimensions": "1:1",
            "art_style": "none",
            "generations_made": 0,
            "chat_history": [],
            "language": "hinglish"
        }
    
    return {
        "safety_mode": bool(row[0]),
        "steps": row[1],
        "dimensions": row[2],
        "art_style": row[3],
        "generations_made": row[4],
        "chat_history": json.loads(row[5]) if row[5] else [],
        "language": row[6] or "hinglish"
    }

# ==================== EXPORT / IMPORT ====================

def export_users_to_txt() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, first_name FROM users ORDER BY user_id")
    users = cursor.fetchall()
    conn.close()
    
    lines = []
    for idx, (uid, username, first_name) in enumerate(users, 1):
        uname = f"@{username}" if username else "No username"
        lines.append(f"#{idx} | {uname} | {uid}")
    
    filename = f"alya_users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    return filename

def import_users_from_txt(file_path: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    added = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            try:
                parts = line.split("|")
                if len(parts) >= 3:
                    uid = int(parts[2].strip())
                    username = parts[1].strip().replace("@", "") if "@" in parts[1] else None
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO users (user_id, username, first_seen, daily_date)
                        VALUES (?, ?, ?, ?)
                    """, (uid, username, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
                    if cursor.rowcount > 0:
                        added += 1
            except:
                continue
    
    conn.commit()
    conn.close()
    return added

# ==================== MEDIA ====================

def add_media(file_id: str, media_type: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO media (type, file_id) VALUES (?, ?)", (media_type, file_id))
    conn.commit()
    conn.close()

def get_random_media(media_type: str) -> Optional[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM media WHERE type = ? ORDER BY RANDOM() LIMIT 1", (media_type,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_media(media_type: str) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM media WHERE type = ?", (media_type,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def remove_media_by_index(media_type: str, index: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM media WHERE type = ? LIMIT 1 OFFSET ?", (media_type, index))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM media WHERE file_id = ?", (row[0],))
    conn.commit()
    conn.close()

# ==================== CHANNELS ====================

def add_channel(channel_id: str, link: str, name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO channels (id, link, name) VALUES (?, ?, ?)", (channel_id, link, name))
    conn.commit()
    conn.close()

def get_channels() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM channels")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def remove_channel(channel_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

# ==================== BLOCKED ====================

def is_blocked(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM blocked WHERE user_id = ?", (str(user_id),))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def block_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO blocked (user_id) VALUES (?)", (str(user_id),))
    conn.commit()
    conn.close()

def unblock_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blocked WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()

# ==================== MOOD ====================

def get_mood() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM mood WHERE key = 'alya_mood'")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "happy"

def set_mood(mood: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mood (key, value, changed_at) 
        VALUES ('alya_mood', ?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value, changed_at = excluded.changed_at
    """, (mood, int(datetime.now().timestamp())))
    conn.commit()
    conn.close()

def should_change_mood() -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT changed_at FROM mood WHERE key = 'alya_mood'")
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return True
    return (datetime.now().timestamp() - row[0]) > (3 * 3600)  # 3 hours

# ==================== ANALYTICS ====================

def track_message():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analytics (date, messages) VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET messages = messages + 1
    """, (today,))
    conn.commit()
    conn.close()

def track_image():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analytics (date, images) VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET images = images + 1
    """, (today,))
    conn.commit()
    conn.close()

print("✅ Database module loaded")
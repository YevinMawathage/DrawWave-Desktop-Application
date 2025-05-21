import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_file='virtual_painter.db'):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create drawings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                color TEXT,
                mode TEXT
            )
        ''')

        # Create settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create drawing_actions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawing_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT NOT NULL,
                points TEXT NOT NULL,
                color TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_drawing(self, filename, color, mode):
        """Save drawing information to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO drawings (filename, color, mode)
            VALUES (?, ?, ?)
        ''', (filename, str(color), mode))
        
        conn.commit()
        conn.close()

    def get_drawings(self):
        """Get all drawings"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM drawings ORDER BY created_at DESC')
        drawings = cursor.fetchall()
        
        conn.close()
        return drawings

    def save_setting(self, name, value):
        """Save a setting"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (name, value, updated_at)
            VALUES (?, ?, ?)
        ''', (name, str(value), datetime.now()))
        
        conn.commit()
        conn.close()

    def get_setting(self, name):
        """Get a setting value"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE name = ?', (name,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None

    def save_action(self, action_type, points, color=None):
        """Save a drawing action"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO drawing_actions (action_type, points, color)
            VALUES (?, ?, ?)
        ''', (action_type, json.dumps(points), json.dumps(color) if color else None))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_all_actions(self):
        """Get all drawing actions"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM drawing_actions ORDER BY id ASC')
        actions = cursor.fetchall()
        
        conn.close()
        return [{
            'id': action[0],
            'action_type': action[1],
            'points': json.loads(action[2]),
            'color': json.loads(action[3]) if action[3] else None,
            'timestamp': action[4]
        } for action in actions]

    def undo_last_action(self):
        """Remove and return the last action"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM drawing_actions ORDER BY id DESC LIMIT 1')
        action = cursor.fetchone()
        
        if action:
            cursor.execute('DELETE FROM drawing_actions WHERE id = ?', (action[0],))
            conn.commit()
            
            conn.close()
            return {
                'action_type': action[1],
                'points': json.loads(action[2]),
                'color': json.loads(action[3]) if action[3] else None
            }
        
        conn.close()
        return None
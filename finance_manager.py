import sqlite3
from datetime import datetime
import bcrypt

class FinanceManager:
    def __init__(self, user_id=None):
        self.conn = sqlite3.connect('finance.db', check_same_thread=False)
        self.user_id = user_id
        self.create_tables()
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='mohamed'")
        if cursor.fetchone()[0] > 0:
            return
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       ('mohamed', bcrypt.hashpw('123'.encode('utf-8'), bcrypt.gensalt())))
        
        # Sample accounts and transactions can be added here...

        self.conn.commit()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    name TEXT,
                    balance REAL,
                    min_balance REAL,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    date TEXT,
                    type TEXT,
                    amount REAL,
                    account_id INTEGER,
                    description TEXT,
                    payment_method TEXT,
                    category TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username),
                    FOREIGN KEY (account_id) REFERENCES accounts(id)
                )
            ''')

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.conn:
            try:
                self.conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def verify_user(self, username, password):
        with self.conn:
            cursor = self.conn.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result and bcrypt.checkpw(password.encode('utf-8'), result[0])

    # Additional methods for account and transaction management...

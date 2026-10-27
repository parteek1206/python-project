"""SQLite module: stores and loads scraped data."""
import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "books.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS books (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   price REAL NOT NULL,
                   rating INTEGER,
                   in_stock INTEGER,
                   image_url TEXT,
                   url TEXT UNIQUE
               )"""
        )


def save_books(books):
    """Insert new books or update existing ones based on URL."""
    init_db()
    with get_connection() as conn:
        before = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        conn.executemany(
            """INSERT INTO books (title, price, rating, in_stock, image_url, url)
               VALUES (:title, :price, :rating, :in_stock, :image_url, :url)
               ON CONFLICT(url) DO UPDATE SET
                   price = excluded.price,
                   rating = excluded.rating,
                   in_stock = excluded.in_stock,
                   image_url = excluded.image_url""",
            books,
        )
        after = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    return after - before


def load_books():
    init_db()
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM books", conn)


def clear_books():
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM books")
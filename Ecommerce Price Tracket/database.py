import sqlite3

def initialize_db():
    """Ensure the database and prices table exist before fetching data."""
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            site TEXT PRIMARY KEY,
            price REAL,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(data):
    initialize_db()  # Ensure table exists before inserting
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    for site, details in data.items():
        cursor.execute("INSERT OR REPLACE INTO prices (site, price, url) VALUES (?, ?, ?)",
                       (site, details["price"], details["url"]))
    
    conn.commit()
    conn.close()

def get_previous_prices():
    initialize_db()  # Ensure table exists before fetching
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT site, price FROM prices ORDER BY timestamp DESC")
    
    prices = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return prices

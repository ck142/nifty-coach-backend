import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Set up database connection (from environment or hardcoded fallback)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tradedb")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def save_trade_to_db(trade):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trades (order_id, symbol, side, qty, price, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
            """,
            (
                trade["order_id"],
                trade["symbol"],
                trade["side"],
                trade["qty"],
                trade["price"],
                trade["timestamp"] if isinstance(trade["timestamp"], datetime) else datetime.now(),
            )
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save trade: {e}")
        return False

def get_all_trades(limit=500):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT %s;", (limit,))
        trades = cursor.fetchall()

        cursor.close()
        conn.close()
        return trades
    except Exception as e:
        print(f"[ERROR] Failed to fetch trades: {e}")
        return []

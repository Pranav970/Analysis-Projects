import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def create_tables():
    """
    Creates the necessary tables in PostgreSQL.
    """
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Create crypto_prices table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                timestamp TIMESTAMP WITHOUT TIME ZONE PRIMARY KEY,
                symbol VARCHAR(10) NOT NULL,
                price NUMERIC NOT NULL,
                volume NUMERIC
            )
        """)

        # Create news_articles table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news_articles (
                article_id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                source VARCHAR(255),
                title TEXT,
                content TEXT,
                cryptocurrency_mentioned VARCHAR(50)
            )
        """)

        conn.commit()
        print("Tables created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    create_tables()

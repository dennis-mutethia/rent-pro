import os, psycopg2
from dotenv import load_dotenv

class PostgresDb:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)
         
       
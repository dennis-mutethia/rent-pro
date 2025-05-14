import os, psycopg2

class PostgresDb:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(self.database_url)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            print(e)
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(self.database_url)
         
       
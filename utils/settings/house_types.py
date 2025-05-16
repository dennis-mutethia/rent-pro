import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import HouseType

class HouseTypes():
    def __init__(self, db): 
        self.db = db
      
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH h AS(
                SELECT house_type_id, COUNT(id) AS houses 
                FROM houses
                GROUP BY house_type_id
            )
            SELECT id, name, description, COALESCE(h.houses, 0)
            FROM house_types 
            LEFT JOIN h ON h.house_type_id = house_types.id
            WHERE company_id = %s
            ORDER BY name
            """
            cursor.execute(query, (current_user.company.id,))
            data = cursor.fetchall()
            house_types = []
            for datum in data:      
                house_types.append(HouseType(datum[0], datum[1], datum[2], datum[3]))
            return house_types  
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, description
            FROM house_types 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return HouseType(data[0], data[1], data[2])
            else:
                return None      
    
    def create(self, id, name, description):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO house_types(id, company_id, name, description, created_at, created_by) 
            VALUES(%s, %s, %s, %s, NOW(), 0)
            """
            params = [id, current_user.company.id, name.upper(), description]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, description):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE house_types 
            SET name=%s,
                description=%s
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [name.upper(), description, current_user.id, id]
            cursor.execute(query, tuple(params))  
            self.db.conn.commit()
        
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM house_types
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
                          
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'create':
                name = request.form['name']
                description = request.form['description']
                id = str(uuid.uuid4())
                self.create(id, name, description)
         
        return render_template('settings/house_types.html', settings=True, house_types=self.fetch())
               
               
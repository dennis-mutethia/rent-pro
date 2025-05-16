
import os
import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import Property
from utils.landlords import Landlords

class Properties():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, landlord_id=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH t AS(
                SELECT house_id, COUNT(id) AS tenants
                FROM tenant_houses
                WHERE DATE(end_date) <= CURRENT_DATE OR end_date IS NULL
                GROUP BY house_id
            ),
            h AS(
                SELECT property_id, COUNT(id) AS houses, SUM(t.tenants) AS tenants
                FROM houses
                LEFT JOIN t ON t.house_id = houses.id
                GROUP BY property_id
            )
            SELECT properties.id, landlord_id, properties.name, location, town, county, lr_no, image, COALESCE(houses, 0), COALESCE(tenants, 0)
            FROM properties 
            INNER JOIN landlords ON landlords.id = properties.landlord_id
            LEFT JOIN h ON h.property_id = properties.id
            WHERE landlords.company_id = %s
            """
            params = [current_user.company.id]
            if landlord_id:
                query += " AND properties.landlord_id = %s"
                params.append(landlord_id)
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            properties = []
            for datum in data:       
                properties.append(Property(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8], datum[9]))

            return properties 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, landlord_id, name, location, town, county, lr_no, image
            FROM properties 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Property(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            else:
                return None      
    
    def create(self, id, landlord_id, name, location, town, county, lr_no, image):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO properties(id, landlord_id, name, location, town, county, lr_no, image, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)
            """
            params = [id, landlord_id, name.upper(), location.upper(), town.upper(), county.upper(), lr_no.upper(), image]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, landlord_id, name, location, town, county, lr_no, image):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE properties 
            SET landlord_id=%s,
                name=%s,
                location=%s,
                town=%s,
                county=%s,
                lr_no=%s,
                image=%s,
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [landlord_id, name.upper(), location.upper(), town.upper(), county.upper(), lr_no.upper(), image, id]
            cursor.execute(query, tuple(params))  
            self.db.conn.commit()
                        
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM properties
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
                          
    def __call__(self):
        landlord_id = request.args.get('landlord_id', None)
        if request.method == 'POST':
            if request.form['action'] == 'create':
                landlord_id = request.form['landlord_id']
                name = request.form['name']
                location = request.form['location']
                town = request.form['town']
                county = request.form['county']
                lr_no = request.form['lr_no']
                image = request.form['image']
                id = str(uuid.uuid4())
                self.create(id, landlord_id, name, location, town, county, lr_no, image)
         
        return render_template('properties.html', imgbb_key=os.getenv('IMGBB_API_KEY'),
                               properties=self.fetch(landlord_id), landlords=Landlords(self.db).fetch())
               
               
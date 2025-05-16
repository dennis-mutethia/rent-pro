import os
import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import Company

class Companies():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH h AS(
                SELECT property_id, COUNT(id) AS houses 
                FROM houses
                GROUP BY property_id
            ),
            p AS(
                SELECT landlord_id, COUNT(id) AS properties, SUM(h.houses) AS houses
                FROM properties
                LEFT JOIN h ON h.property_id = properties.id
                GROUP BY landlord_id
            ),
            l AS(
                SELECT company_id, COUNT(id) AS landlords, SUM(p.properties) AS properties, SUM(p.houses) AS houses
                FROM landlords 
                LEFT JOIN p ON p.landlord_id = landlords.id
                GROUP BY company_id
            )
            SELECT id, name, phone, COALESCE(landlords, 0), COALESCE(properties, 0), COALESCE(houses, 0)
            FROM companies 
            LEFT JOIN l ON l.company_id = companies.id
            """
            cursor.execute(query)
            data = cursor.fetchall()
            companies = []
            for datum in data:       
                companies.append(Company(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5]))

            return companies 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone
            FROM companies 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Company(data[0], data[1], data[2])
            else:
                return None      
    
    def create(self, id, name, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO companies(id, name, phone, created_at, created_by) 
            VALUES(%s, %s, %s, NOW(), 0)
            """
            params = [id, name.upper(), phone]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE companies 
            SET name=%s,
                phone=%s
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [name.upper(), phone, current_user.id, id]
            cursor.execute(query, tuple(params))  
            self.db.conn.commit()
                        
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM companies
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
                          
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'create':
                company_name = request.form['name']
                phone = request.form['phone']
                company_id = str(uuid.uuid4())
                self.create(company_id, company_name, phone)
         
        return render_template('companies.html', companies=self.fetch())
               
import os
import uuid
from flask import render_template, request
from flask_login import current_user

from utils.companies import Companies
from utils.entities import Landlord

class Landlords():
    def __init__(self, db): 
        self.db = db
        self.companies = Companies(self.db)
            
    def fetch(self):
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
            ),
            p AS(
                SELECT landlord_id, COUNT(id) AS properties, SUM(h.houses) AS houses, SUM(h.tenants) AS tenants
                FROM properties
                LEFT JOIN h ON h.property_id = properties.id
                GROUP BY landlord_id
            )
            
            SELECT id, name, phone, company_id, COALESCE(properties, 0), COALESCE(houses, 0), COALESCE(tenants, 0)
            FROM landlords
            LEFT JOIN p ON p.landlord_id = landlords.id
            WHERE company_id = %s 
            """
            cursor.execute(query, (current_user.company.id,))
            data = cursor.fetchall()
            companies = []
            for datum in data:       
                companies.append(Landlord(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6]))

            return companies 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, company_id
            FROM landlords 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Landlord(data[0], data[1], data[2], data[3])
            else:
                return None      
    
    def create(self, id, name, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO landlords(id, name, phone, company_id, created_at, created_by) 
            VALUES(%s, %s, %s, %s, NOW(), %s)
            """
            params = [id, name.upper(), phone, current_user.company.id, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE landlords 
            SET name=%s,
                phone=%s,
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
            DELETE FROM landlords
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
                          
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'create':
                name = request.form['name']
                phone = request.form['phone']
                id = str(uuid.uuid4())
                self.create(id, name, phone)
        
        return render_template('landlords.html', landlords=self.fetch())
               
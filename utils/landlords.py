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
            
    def fetch(self, company_id=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, company_id
            FROM landlords 
            """
            if company_id:
                query += " WHERE company_id = %s"
                cursor.execute(query, (company_id,))
            else:
                cursor.execute(query)
            data = cursor.fetchall()
            companies = []
            for datum in data:       
                companies.append(Landlord(datum[0], datum[1], datum[2], datum[3]))

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
    
    def create(self, id, name, phone, company_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO landlords(id, name, phone, company_id, created_at, created_by) 
            VALUES(%s, %s, %s, %s, NOW(), 0)
            """
            params = [id, name.upper(), phone, company_id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, phone, company_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE landlords 
            SET name=%s,
                phone=%s,
                company_id=%s,
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [name.upper(), phone, company_id, current_user.id, id]
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
        company_id=request.args.get('company_id', None)
        if request.method == 'POST':
            if request.form['action'] == 'create':
                name = request.form['name']
                phone = request.form['phone']
                new_company_id = request.form['company_id']
                id = str(uuid.uuid4())
                self.create(id, name, phone, new_company_id)
        
        return render_template('landlords.html', imgbb_key=os.getenv('IMGBB_API_KEY'),
                               landlords=self.fetch(company_id), companies=self.companies.fetch(), company_id=company_id
                               )
               

import os
import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import House, Property
from utils.landlords import Landlords
from utils.properties import Properties
from utils.settings.house_types import HouseTypes

class Houses():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, property_id=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH th AS(
                SELECT house_id, tenant_id, 
                    CASE 
                        WHEN DATE(end_date) < CURRENT_DATE THEN 'VACANT' 
                        ELSE 'OCCUPIED' 
                    END AS status
                FROM tenant_houses
            ),
            t AS(
                SELECT house_id, tenant_id, status, name, phone
                FROM tenants
                INNER JOIN th ON th.tenant_id = tenants.id
            )
            SELECT houses.id, property_id, house_type_id, houses.name, rent_amount, deposit_amount, COALESCE(t.status, 'VACANT'), tenant_id, t.name, t.phone
            FROM houses 
            INNER JOIN properties ON properties.id = houses.property_id
            INNER JOIN landlords ON landlords.id = properties.landlord_id
            LEFT JOIN t ON t.house_id = houses.id
            WHERE landlords.company_id = %s
            """
            params = [current_user.company.id]
            if property_id:
                query += " AND houses.property_id = %s"
                params.append(property_id)
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            houses = []
            for datum in data:       
                houses.append(House(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8], datum[9]))

            return houses 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, property_id, house_type_id, name, rent_amount, deposit_amount
            FROM houses 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return House(data[0], data[1], data[2], data[3], data[4], data[5])
            else:
                return None      
    
    def create(self, id, property_id, house_type_id, name, rent_amount, deposit_amount):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO houses(id, property_id, house_type_id, name, rent_amount, deposit_amount, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, %s, NOW(), %s)
            """
            params = [id, property_id, house_type_id, name.upper(), rent_amount, deposit_amount, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, property_id, house_type_id, name, rent_amount, deposit_amount):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE houses 
            SET property_id=%s,
                house_type_id=%s,
                name=%s,
                rent_amount=%s,
                deposit_amount=%s,
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [property_id, house_type_id, name.upper(), rent_amount, deposit_amount, current_user.id, id]
            cursor.execute(query, tuple(params))  
            self.db.conn.commit()
                        
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM houses
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
                          
    def __call__(self):
        property_id = request.args.get('property_id', None)
        if request.method == 'POST':
            if request.form['action'] == 'create':                
                property_id = request.form['property_id']
                house_type_id = request.form['house_type_id']
                name = request.form['name']
                rent_amount = request.form['rent_amount']
                deposit_amount = request.form['deposit_amount']
                id = str(uuid.uuid4())
                self.create(id, property_id, house_type_id, name, rent_amount, deposit_amount)
         
        return render_template('houses.html', houses=self.fetch(property_id), house_types = HouseTypes(self.db).fetch(), properties=Properties(self.db).fetch())
               
               
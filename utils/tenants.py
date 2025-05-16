
import os
import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import House, Tenant
from utils.houses import Houses

class Tenants():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, house_id=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH th AS(
                SELECT house_id, tenant_id, start_date,
                    CASE 
                        WHEN DATE(end_date) < CURRENT_DATE THEN 'VACATED' 
                        ELSE 'OCCUPIED' 
                    END AS status, end_date, houses.name AS house_name, property_id, properties.name AS property_name, location, town, county                    
                FROM tenant_houses
                INNER JOIN houses ON houses.id = tenant_houses.house_id
                INNER JOIN properties ON properties.id = houses.property_id
                INNER JOIN landlords ON landlords.id = properties.landlord_id
                WHERE landlords.company_id = %s
            )
            SELECT tenants.id, name, phone, email, id_number, DATE(start_date), status, DATE(end_date), image, next_of_kin, next_of_kin_phone, house_id, house_name, property_id, property_name, location, town, county
            FROM tenants
            INNER JOIN th ON th.tenant_id = tenants.id
            WHERE 1=1
            """
            params = [current_user.company.id]
            if house_id:
                query += " AND th.house_id = %s"
                params.append(house_id)
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            tenants = []
            for datum in data:   
                tenants.append(Tenant(
                    datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8], datum[9], 
                    datum[10], datum[11], datum[12], datum[13], datum[14], datum[15], datum[16], datum[17]
                ))

            return tenants 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, email, next_of_kin, next_of_kin_phone
            FROM tenants 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Tenant(data[0], data[1], data[2], data[3], data[4], data[5])
            else:
                return None      
    
    def create(self, id, house_id, name, id_number, phone, email, image, next_of_kin, next_of_kin_phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO tenants(id, name, id_number, phone, email, image, next_of_kin, next_of_kin_phone, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
            """
            params = [id, name, id_number, phone, email, image, next_of_kin, next_of_kin_phone, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
            query = """
            INSERT INTO tenant_houses(id, tenant_id, house_id, start_date, created_at, created_by) 
            VALUES(%s, %s, %s, NOW(), NOW(), %s)
            """
            params = [str(uuid.uuid4()), id, house_id, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, id_number, phone, email, image, next_of_kin, next_of_kin_phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE tenants 
            SET name=%s,
                id_number=%s,
                phone=%s,
                email=%s,
                image=%s,
                next_of_kin=%s,
                next_of_kin_phone=%s,
                updated_by=%s,
                updated_at=NOW()  
            WHERE id=%s     
            """
            params = [name.upper(), id_number, phone, email, image, next_of_kin, next_of_kin_phone, current_user.id, id]
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
        house_id = request.args.get('house_id', None)
        if request.method == 'POST':
            if request.form['action'] == 'create':                
                house_id = request.form['house_id']
                name = request.form['name']
                id_number = request.form['id_number']
                phone = request.form['phone']
                email = request.form['email']
                image = request.form['image']
                next_of_kin = request.form['next_of_kin']
                next_of_kin_phone = request.form['next_of_kin_phone']
                id = str(uuid.uuid4())
                self.create(id, house_id, name, id_number, phone, email, image, next_of_kin, next_of_kin_phone)
         
        return render_template('tenants.html', imgbb_key=os.getenv('IMGBB_API_KEY'),
                               tenants=self.fetch(house_id), houses = Houses(self.db).fetch())
               
               
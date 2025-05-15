import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import User, UserLevel
from utils.helper import Helper

class SystemUsers():
    def __init__(self, db): 
        self.db = db
      
    def fetch_user_levels(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, level, description
            FROM user_levels 
            ORDER BY id
            """
            cursor.execute(query)
            data = cursor.fetchall()
            user_levels = []
            for datum in data:      
                user_levels.append(UserLevel(datum[0], datum[1], datum[2], datum[3]))

            return user_levels 
        
    def get_user_level_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, level, description
            FROM user_levels 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return UserLevel(data[0], data[1], data[2], data[3])
            else:
                return None    
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, building_id
            FROM users 
            WHERE building_id IN(
                SELECT id FROM shops WHERE company_id = %s
            )
            """
            params = [current_user.company.id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            users = []
            for datum in data:      
                user_level = self.get_user_level_id(datum[3])
                shop = None #MyShops(self.db).get_by_id(datum[4]) 
                company = None #self.db.get_company_by_id(shop.company_id)
                license = None #self.db.get_license_by_id(company.license_id)   
                users.append(User(datum[0], datum[1], datum[2], user_level, shop, company, license))

            return users 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, building_id
            FROM users 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level_id(data[3])
                shop = None #MyShops(self.db).get_by_id(data[4])
                company = None #self.db.get_company_by_id(shop.company_id)
                license = None #self.db.get_license_by_id(company.license_id)   
                return User(data[0], data[1], data[2], user_level, shop, company, license)
            else:
                return None      
    
    def get_by_phone(self, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, building_id
            FROM users 
            WHERE phone = %s 
            """
            cursor.execute(query, (phone,))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level_id(data[3])
                shop = None #MyShops(self.db).get_by_id(data[4])
                company = None #self.db.get_company_by_id(shop.company_id)
                license = None #self.db.get_license_by_id(company.license_id)   
                return User(data[0], data[1], data[2], user_level, shop, company, license)
            else:
                return None    
           
    def authenticate(self, phone, password):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, building_id
            FROM users 
            WHERE phone = %s AND password = %s 
            """
            cursor.execute(query, (phone, Helper().hash_password(password)))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level_id(data[3])
                shop = None #MyShops(self.db).get_by_id(data[4])
                company = None #self.db.get_company_by_id(shop.company_id)
                license = None #self.db.get_license_by_id(company.license_id)   
                return User(data[0], data[1], data[2], user_level, shop, company, license)
            else:
                return None 
    
    def create(self, id, name, phone, user_level_id, building_id, password):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO users(id, name, phone, user_level_id, building_id, password, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, %s, NOW(), 0)
            ON CONFLICT (phone)
                DO UPDATE SET 
                    name=%s,
                    user_level_id=%s,
                    building_id=%s,
                    updated_at=NOW()
            RETURNING id
            """
            cursor.execute(query, (id, name.upper(), phone, user_level_id, building_id, Helper().hash_password(password), name.upper(), user_level_id, building_id))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, user_id, name, phone, user_level_id, building_id, password):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE users 
            SET name = %s, phone = %s, user_level_id = %s, building_id = %s, updated_by = %s, updated_at=NOW()            
            """
            params = [name.upper(), phone, user_level_id, building_id, current_user.id]
            if password is not None:
                query = query + ", password = %s"
                params.append(Helper().hash_password(password))
            
            query = query + " WHERE id=%s"
            params.append(user_id)
            
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
    def reset_password(self, phone, password, updated_by):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE users 
            SET password = %s, updated_by = %s, updated_at=NOW()   
            WHERE phone = %s         
            """
            params = [Helper().hash_password(password), updated_by, phone]            
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM users
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
               
    def __call__(self):                
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                user_id = str(uuid.uuid4())
                name = request.form['name']
                phone = request.form['phone']      
                user_level_id = request.form['user_level_id']     
                building_id = request.form['building_id']  
                self.create(user_id, name, phone, user_level_id, building_id, password=phone)
                   
            if request.form['action'] == 'edit':
                user_id = request.form['id']
                name = request.form['name']
                phone = request.form['phone']      
                user_level_id = request.form['user_level_id']     
                building_id = request.form['building_id']                     
                self.update(user_id, name, phone, user_level_id, building_id, password=None)
                
            if request.form['action'] == 'reset_password':
                phone = request.form['phone']                    
                self.reset_password(phone, phone, current_user.id)                 
                
            elif request.form['action'] == 'delete':
                user_id = request.form['id']
                self.delete(user_id)
                
                
        users = self.fetch() 
        user_levels = self.fetch_user_levels()
        company_shops = self.db.get_company_shops()
            
        return render_template('settings/system-users.html', page_title='System Users', helper=Helper(),
                               users=users, user_levels=user_levels, company_shops=company_shops )
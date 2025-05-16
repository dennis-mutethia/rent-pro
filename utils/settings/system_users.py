import uuid
from flask import render_template, request
from flask_login import current_user

from utils.entities import User, UserLevel
from utils.helper import Helper
from utils.companies import Companies

class SystemUsers():
    def __init__(self, db): 
        self.db = db
        self.companies = Companies(self.db)
      
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
        
    def get_user_level(self, level):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, level, description
            FROM user_levels 
            WHERE level = %s 
            """
            cursor.execute(query, (level,))
            data = cursor.fetchone()
            if data:
                return UserLevel(data[0], data[1], data[2], data[3])
            else:
                return None    
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, password, company_id, landlord_id, property_id
            FROM users 
            """
            
            cursor.execute(query)
            data = cursor.fetchall()
            users = []
            for datum in data:      
                user_level = self.get_user_level(datum[3])
                company = self.companies.get_by_id(datum[5])
                landlord = None 
                property = None 
                users.append(User(datum[0], datum[1], datum[2], user_level, company, landlord, property))

            return users 
               
    def get_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, password, company_id, landlord_id, property_id
            FROM users 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level(data[3])
                company = self.companies.get_by_id(data[5])
                landlord = None 
                property = None 
                return User(data[0], data[1], data[2], user_level, company, landlord, property)
            else:
                return None      
    
    def get_by_phone(self, phone):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, password, company_id, landlord_id, property_id
            FROM users 
            WHERE phone = %s 
            """
            cursor.execute(query, (phone,))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level(data[3])
                company = self.companies.get_by_id(data[5])
                landlord = None 
                property = None 
                return User(data[0], data[1], data[2], user_level, company, landlord, property)
            else:
                return None    
           
    def authenticate(self, phone, password):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, password, company_id, landlord_id, property_id
            FROM users 
            WHERE phone = %s AND password = %s 
            """
            cursor.execute(query, (phone, Helper().hash_password(password)))
            data = cursor.fetchone()
            if data:
                user_level = self.get_user_level(data[3])
                company = self.companies.get_by_id(data[5])
                landlord = None 
                property = None 
                return User(data[0], data[1], data[2], user_level, company, landlord, property)
            else:
                return None 
    
    def create(self, id, name, phone, password, user_level_id, company_id, landlord_id=None, property_id=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO users(id, name, phone, user_level_id, password, company_id, landlord_id, property_id, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)
            """
            params = [id, name.upper(), phone, user_level_id, Helper().hash_password(password), company_id, landlord_id, property_id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            return self.get_by_id(id)  
            
    def update(self, id, name, phone, user_level_id, company_id, landlord_id, property_id, password=None):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE users 
            SET name=%s,
                phone=%s,
                user_level_id=%s,
                company_id=%s,
                landlord_id=%s,
                property_id=%s,
                updated_by=%s,
                updated_at=NOW()       
            """
            params = [name.upper(), phone, user_level_id, company_id, landlord_id, property_id, current_user.id]  
            if password is not None:
                query = query + ", password=%s"
                params.append(Helper().hash_password(password))
            
            query = query + " WHERE id=%s"
            params.append(id)
            
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
               
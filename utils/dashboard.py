
from datetime import datetime, timedelta
from flask import render_template, request
from flask_login import current_user

class Dashboard():
    def __init__(self, db): 
        self.db = db        
    
    def total_landlords(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT COUNT(id)
            FROM landlords
            WHERE company_id = %s
            """ 
            params = [current_user.company.id]
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return 0   
    
    def total_properties(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT COUNT(properties.id)
            FROM properties
            INNER JOIN landlords ON landlords.id = properties.landlord_id
            WHERE landlords.company_id = %s
            """
            params = [current_user.company.id]
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return 0
    
    def total_houses(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT COUNT(houses.id)
            FROM houses
            INNER JOIN properties ON properties.id = houses.property_id
            INNER JOIN landlords ON landlords.id = properties.landlord_id
            WHERE landlords.company_id = %s
            """
            params = [current_user.company.id]
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return 0
    
    def total_tenants(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT COUNT(houses.id)
            FROM tenant_houses
            INNER JOIN houses ON houses.id = tenant_houses.house_id
            INNER JOIN properties ON properties.id = houses.property_id
            INNER JOIN landlords ON landlords.id = properties.landlord_id
            WHERE landlords.company_id = %s AND (DATE(end_date) <= CURRENT_DATE OR DATE(end_date) IS NULL)
            """
            params = [current_user.company.id]
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return 0
            
    def get_company_counts(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
                WITH landlord_data AS (
                    SELECT id
                    FROM landlords
                    WHERE company_id = %s
                ),
                property_data AS (
                    SELECT properties.id
                    FROM properties
                    INNER JOIN landlord_data ON landlord_data.id = properties.landlord_id
                ),
                house_data AS (
                    SELECT houses.id
                    FROM houses
                    INNER JOIN property_data ON property_data.id = houses.property_id
                ),
                tenant_data AS (
                    SELECT house_data.id
                    FROM tenant_houses
                    INNER JOIN house_data ON house_data.id = tenant_houses.house_id
                    WHERE DATE(tenant_houses.end_date) <= CURRENT_DATE OR tenant_houses.end_date IS NULL
                )
                SELECT 
                    (SELECT COUNT(*) FROM landlord_data) AS landlord_count,
                    (SELECT COUNT(*) FROM property_data) AS property_count,
                    (SELECT COUNT(*) FROM house_data) AS house_count,
                    (SELECT COUNT(*) FROM tenant_data) AS tenant_count
                """
            params = [current_user.company.id]
            cursor.execute(query, params)
            data = cursor.fetchone()
            return data[0] if data else 0, data[1] if data else 0, data[2] if data else 0, data[3] if data else 0            
                
    def __call__(self):
        landlords, properties, houses, tenants = self.get_company_counts()
         
        return render_template('dashboard.html', landlords=landlords, properties=properties,  houses=houses, tenants=tenants )
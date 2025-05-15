from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, phone, user_level, company, landlord, property):  
        self.id = id
        self.name = name
        self.phone = phone
        self.user_level = user_level
        self.company = company 
        self.landlord = landlord
        self.property = property

class UserLevel():
    def __init__(self, id, name, level, description):
        self.id = id
        self.name = name
        self.level = level
        self.description = description 
class Company():
    def __init__(self, id, name, phone, landlords=0, properties=0, houses=0, tenants=0):
        self.id = id
        self.name = name
        self.phone = phone
        self.landlords = landlords
        self.properties = properties
        self.houses = houses
        self.tenants = tenants        
class Landlord():
    def __init__(self, id, name, phone, company_id=None, properties=0, houses=0, tenants=0):
        self.id = id
        self.name = name
        self.phone = phone
        self.company_id = company_id
        self.properties = properties
        self.houses = houses
        self.tenants = tenants
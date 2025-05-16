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
class Property():
    def __init__(self, id, landlord_id, name, location, town, county, lr_no, image, houses=0, tenants=0):
        self.id = id
        self.landlord_id = landlord_id
        self.name = name
        self.location = location
        self.town = town
        self.county = county
        self.lr_no = lr_no
        self.image = image
        self.houses = houses
        self.tenants = tenants   
        
class HouseType():
    def __init__(self, id, name, description, houses=0):
        self.id = id
        self.name = name
        self.description = description
        self.houses = houses 
class House():
    def __init__(self, id, property_id, house_type_id, name, rent_amount, deposit_amount, status='VACANT', tenant_id=None, tenant_name=None, tenant_phone=None):
        self.id = id
        self.property_id = property_id
        self.house_type_id = house_type_id  
        self.name = name 
        self.rent_amount = rent_amount
        self.deposit_amount = deposit_amount
        self.status = status
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.tenant_phone = tenant_phone
        
class Tenant():
    def __init__(self, id, name, phone, email, id_number, start_date, status='OCCUPIED', end_date=None, image=None, next_of_kin=None, next_of_kin_phone=None, house_id=None, house_name=None, property_id=None, property_name=None, location=None, town=None, county=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.id_number = id_number
        self.start_date = start_date
        self.status = status
        self.end_date = end_date
        self.image = image
        self.next_of_kin = next_of_kin
        self.next_of_kin_phone = next_of_kin_phone
        self.house_id = house_id
        self.house_name = house_name
        self.property_id = property_id
        self.property_name = property_name
        self.location = location
        self.town = town
        self.county = county
        
        

  

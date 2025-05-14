from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, phone, user_level, shop, company, license):  
        self.id = id
        self.name = name
        self.phone = phone
        self.user_level = user_level
        self.shop = shop 
        self.company = company 
        self.license = license

class UserLevel():
    def __init__(self, id, name, level, description):
        self.id = id
        self.name = name
        self.level = level
        self.description = description 
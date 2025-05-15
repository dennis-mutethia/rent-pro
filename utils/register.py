import uuid
from flask import redirect, render_template, request, url_for
from flask_login import login_user

from utils.settings.system_users import SystemUsers

class Register():
    def __init__(self, db): 
        self.db = db     
    
    def register(self):           
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']    
        if not phone or not password or not confirm_password:
            return render_template('register.html', error='Please fill in all fields.')
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match.')
        else:
            # Check if the phone number already exists
            if SystemUsers(self.db).get_by_phone(phone):
                return render_template('register.html', error='Phone number already exists.')
                        
            # Create a new user
            user_id = str(uuid.uuid4())
            user_level_id = 1  # Admin
            building_id = ''
            new_user = SystemUsers(self.db).create(user_id, name, phone, user_level_id, building_id, password)
            
            # Log in the new user
            login_user(new_user)
            return redirect(url_for('dashboard'))         
    
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'register':
                return self.register()

        return render_template('register.html', error=None)

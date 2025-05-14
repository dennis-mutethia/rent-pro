import pytz, random
from datetime import datetime
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user

from utils.settings.system_users import SystemUsers

class Login():
    def __init__(self, db): 
        self.db = db        
     
    def login(self):  
        phone = request.form['phone']
        password = request.form['password']   
        if SystemUsers(self.db).get_by_phone(phone):            
            user = SystemUsers(self.db).authenticate(phone, password)
        
            if user:        
                login_user(user)
                return redirect(url_for('dashboard'))
            else: 
                error = 'Login failed! Phone & Password do not match.'
                return render_template('login.html', error=error)
        else:
            error = 'Login failed! Phone does not exist.'
            return render_template('login.html', error=error)
    
    def reset_password(self):
        phone = request.form['phone']
        password = str(random.randint(1000, 9999))
        print(password)
        ## send SMS
        return render_template('login.html')
     
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'login':
                return self.login()
            elif request.form['action'] == 'reset_password':
                return self.reset_password()

        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=None)

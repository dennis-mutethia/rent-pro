import pytz, random
from datetime import datetime
from flask import redirect, render_template, request, url_for
from flask_login import login_user

from utils.settings.system_users import SystemUsers

class Register():
    def __init__(self, db): 
        self.db = db     
    
    def register(self):           
        phone = request.form['phone']
        password = request.form['password']
        #register logic
        return redirect(url_for('dashboard'))         
    
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'register':
                return self.register()

        return render_template('register.html', error=None)

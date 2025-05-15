
from datetime import datetime, timedelta
from flask import render_template, request
from flask_login import current_user

class Properties():
    def __init__(self, db): 
        self.db = db
                
    def __call__(self):
         
        return render_template('properties.html', page_title='Properties')
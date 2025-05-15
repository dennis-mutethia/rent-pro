
from datetime import datetime, timedelta
import os
from flask import render_template, request
from flask_login import current_user

class Properties():
    def __init__(self, db): 
        self.db = db
                
    def __call__(self):
         
        return render_template('properties.html', imgbb_key=os.getenv('IMGBB_API_KEY'),
                               page_title='Properties')
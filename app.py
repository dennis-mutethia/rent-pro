import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, send_from_directory
from flask_login import LoginManager, logout_user, login_required
from flask_session import Session
from redis import Redis

from utils.dashboard import Dashboard
from utils.login import Login
from utils.postgres_db import PostgresDb
from utils.properties import Properties
from utils.register import Register
from utils.settings.system_users import SystemUsers

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

# Load environment variables from .env file
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(
    host=os.getenv('REDIS_HOSTNAME'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD') if os.getenv('REDIS_SSL') in ['True', '1'] else None,
    ssl=False if os.getenv('REDIS_SSL') in ['False', '0'] else True
)

app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS on Vercel
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = PostgresDb()
#db.migration()
         
# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return SystemUsers(db).get_by_id(user_id)

@app.errorhandler(404)
def page_not_found(e):
    # Redirect to a specific endpoint, like 'plans', or a custom 404 page
    return redirect(url_for('login'), 302)

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return Login(db)()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return Register(db)()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard(): 
    return Dashboard(db)() 

@app.route('/properties', methods=['GET', 'POST'])
@login_required
def properties(): 
    return Properties(db)() 

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', '1', 't']
    app.run(debug=debug_mode)

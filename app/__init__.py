from flask import Flask
from app.ext import db, migrate
from app.blueprints import bps
from app.mail import mail
from flask import request 
from app.cache import cache

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("config")
    
    db.configure(app)
    migrate.configure(app)

    mail.configure(app)
    bps.configure(app)
    cache.configure(app)
    
    return app

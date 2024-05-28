# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:40:30 2024

@author: Usha.HN
"""

# main_app.py
from flask import Flask
from auth_app.auth import auth_bp
from data_app.data import data_bp

def create_app():
    app = Flask(__name__)
    # app.secret_key = 'your_secret_key_here'
    app.secret_key = "3704de6505814e27493a7cc35a10e1aebd9316173a6b7451f7fc69246aef5504"
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_bp, url_prefix='/data')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

import firebase_admin
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
# default_apps = initialize_app()


def create_app():   
    app = Flask(__name__)
    CORS(app, origins='http://localhost:3000')
    app.config ['SECRET_KEY'] = '12345qwerty'

    from userAPI import userAPI
    from dataAPI import dataAPI

    app.register_blueprint(userAPI, url_prefix= '/user')
    app.register_blueprint(dataAPI, url_prefix= '/data')

    return app


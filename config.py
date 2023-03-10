from flask import Flask
from routes import views
from models import db
from schema import ma
import os
from auth import login_manager
from auth import Auth
from admin import admin
import connexion


basedir = os.path.abspath(os.path.dirname(__file__))
application = connexion.FlaskApp(__name__)
application.add_api("swagger.yaml")
app = application.app
# init section
UPLOAD_FOLDER = os.path.join(app.root_path,"uploads")
db.init_app(app)
login_manager.init_app(app)
admin.init_app(app)
ma.init_app(app)
# init section 
app.secret_key=os.urandom(16)
basepath=app.root_path
DATABASE_FOLDER=basepath+'/Database'
os.makedirs(DATABASE_FOLDER,exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(DATABASE_FOLDER, 'Database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(Auth,url_prefix='/auth')
app.register_blueprint(blueprint=views,url_prefix='/')








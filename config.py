from flask import Flask
from routes import views
from models import db
import os
from auth import login_manager
from auth import Auth
# from admin import admin



app=Flask(__name__)
# init section
db.init_app(app)
login_manager.init_app(app)

app.secret_key="easyconnect"
basepath=app.root_path
DATABASE_FOLDER=basepath+'/Database'
os.makedirs(DATABASE_FOLDER,exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(DATABASE_FOLDER, 'Database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.register_blueprint(Auth,url_prefix='/auth')
app.register_blueprint(blueprint=views,url_prefix='/')




# Made with ❤ By mangal
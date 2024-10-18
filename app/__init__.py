from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_migrate import Migrate
from app.MachineLearn import MachineLearn
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os

load_dotenv()
application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(os.getenv('PERMANENT_SESSION_LIFETIME')))
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(application)
migrate = Migrate(application, db)
projeto = MachineLearn()
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'


from app.controllers.ControllerRegisterNF import *
from app.controllers.ControllerLogin import *
from app.controllers.ControllerUser import *
from app.controllers.ControllerPrevisao import *
from app.models import *

@login_manager.user_loader
def load_user(userId):
     return User.query.get(int(userId))

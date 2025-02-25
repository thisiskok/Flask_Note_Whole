from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

#Initialize Extensions and Constants
db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

#create_app function
def create_app(): #create a fully configured Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #Security key for sessions and cookies
    
    # 获取数据库URL并处理postgres://前缀
    DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    print("Using database:", DATABASE_URL)  # 添加这行来显示实际使用的数据库
    
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app) #binds the database instance to the Flask app

    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    #url_prefix is optional for all the blueprint's routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    #creates all database tables defined in the models if they don't already exist
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'#the endpoint to redirect to if the user needs to log in
    login_manager.init_app(app)#Bind the login manager to the Flask app

    #Define a user loader callback for Flask-Login to load a user by their ID from the database
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app): #access the app's context and database configuration
    if not path.exists('website/' + DB_NAME): #if it exists using path.exists('website/' + DB_NAME)
        with app.app_context(): #If it does not exist, it creates the database and its tables within an application context
            db.create_all()
        print('Created Database!')


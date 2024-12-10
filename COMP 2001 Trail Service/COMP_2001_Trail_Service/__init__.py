import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://WKeogh:BfcK306+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_WKeogh"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.engine.connect() 
        print("Database connected successfully!")
    except Exception as e:
        print("Error connecting to the database:", e)

load_dotenv()  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

from COMP_2001_Trail_Service import views
from COMP_2001_Trail_Service import models
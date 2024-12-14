import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.engine.connect() 
        print(app.url_map)
        print("Database connected successfully!")
    except Exception as e:
        print("Error connecting to the database:", e)

print("Registered Routes:")
for rule in app.url_map.iter_rules():
    print(rule)

from COMP_2001_Trail_Service import views
from COMP_2001_Trail_Service import models

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
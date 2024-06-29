
     
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Product, Category, Order, OrderItem, Review
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
migrate = Migrate(app, db)
 
db.init_app(app)
 
 
@app.route('/')
def hello_world():
    return 'Welcome to Interior Designs Store'
 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
 
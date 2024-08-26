from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from models import db, User, Product, Category, Order, OrderItem, Review  # Adjust imports as per your project structure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Change to your database URI if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

def seed_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed users
        users = [
            User(firstname="John", lastname="Doe", username="johndoe", email="johndoe@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Jane", lastname="Smith", username="janesmith", email="janesmith@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Alice", lastname="Brown", username="alicebrown", email="alicebrown@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Bob", lastname="Jones", username="bobjones", email="bobjones@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Charlie", lastname="Davis", username="charliedavis", email="charliedavis@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="David", lastname="Evans", username="davidevans", email="davidevans@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Eve", lastname="Green", username="evegreen", email="evegreen@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Frank", lastname="Harris", username="frankharris", email="frankharris@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Grace", lastname="Ivy", username="graceivy", email="graceivy@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8')),
            User(firstname="Henry", lastname="James", username="henryjames", email="henryjames@example.com", password_hash=bcrypt.generate_password_hash("password").decode('utf-8'))
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()

        # Seed categories
        categories = [
            Category(name="Living Room"),
            Category(name="Bedroom"),
            Category(name="Kitchen"),
            Category(name="Bathroom"),
            Category(name="Office"),
            Category(name="Outdoor"),
            Category(name="Lighting"),
            Category(name="Decor"),
            Category(name="Furniture"),
            Category(name="Storage")
        ]

        db.session.bulk_save_objects(categories)
        db.session.commit()

        # Seed products
        products = [
            Product(name="Sofa", description="A comfortable three-seater sofa.", price=500.0, category_id=1),
            Product(name="Bed", description="A king-sized bed with storage.", price=1000.0, category_id=2),
            Product(name="Dining Table", description="A wooden dining table for six.", price=750.0, category_id=3),
            Product(name="Shower Curtain", description="A waterproof shower curtain.", price=20.0, category_id=4),
            Product(name="Office Chair", description="An ergonomic office chair.", price=150.0, category_id=5),
            Product(name="Patio Set", description="An outdoor patio set with table and chairs.", price=300.0, category_id=6),
            Product(name="Chandelier", description="A modern chandelier with LED lights.", price=200.0, category_id=7),
            Product(name="Wall Art", description="A set of three abstract wall art pieces.", price=100.0, category_id=8),
            Product(name="Bookshelf", description="A tall wooden bookshelf.", price=250.0, category_id=9),
            Product(name="Wardrobe", description="A spacious wardrobe with sliding doors.", price=800.0, category_id=10)
        ]

        db.session.bulk_save_objects(products)
        db.session.commit()

        # Seed orders
        orders = [
            Order(user_id=1, total_price=520.0, status="Completed"),
            Order(user_id=2, total_price=1150.0, status="Processing"),
            Order(user_id=3, total_price=770.0, status="Completed"),
            Order(user_id=4, total_price=170.0, status="Shipped"),
            Order(user_id=5, total_price=1250.0, status="Completed"),
            Order(user_id=6, total_price=350.0, status="Processing"),
            Order(user_id=7, total_price=220.0, status="Shipped"),
            Order(user_id=8, total_price=900.0, status="Completed"),
            Order(user_id=9, total_price=150.0, status="Processing"),
            Order(user_id=10, total_price=1050.0, status="Shipped")
        ]

        db.session.bulk_save_objects(orders)
        db.session.commit()

        # Seed order items
        order_items = [
            OrderItem(order_id=1, product_id=1, quantity=1, price=500.0),
            OrderItem(order_id=1, product_id=4, quantity=1, price=20.0),
            OrderItem(order_id=2, product_id=2, quantity=1, price=1000.0),
            OrderItem(order_id=2, product_id=5, quantity=1, price=150.0),
            OrderItem(order_id=3, product_id=3, quantity=1, price=750.0),
            OrderItem(order_id=3, product_id=7, quantity=1, price=20.0),
            OrderItem(order_id=4, product_id=8, quantity=1, price=100.0),
            OrderItem(order_id=4, product_id=6, quantity=1, price=70.0),
            OrderItem(order_id=5, product_id=9, quantity=1, price=250.0),
            OrderItem(order_id=5, product_id=10, quantity=1, price=1000.0),
            OrderItem(order_id=6, product_id=3, quantity=1, price=750.0),
            OrderItem(order_id=7, product_id=2, quantity=1, price=1000.0),
            OrderItem(order_id=8, product_id=1, quantity=1, price=500.0),
            OrderItem(order_id=9, product_id=4, quantity=1, price=20.0),
            OrderItem(order_id=10, product_id=5, quantity=1, price=150.0)
        ]

        db.session.bulk_save_objects(order_items)
        db.session.commit()

        # Seed reviews
        reviews = [
            Review(user_id=1, product_id=1, rating=5, comment="Excellent sofa!"),
            Review(user_id=2, product_id=2, rating=4, comment="Great bed."),
            Review(user_id=3, product_id=3, rating=5, comment="Loved this dining table."),
            Review(user_id=4, product_id=4, rating=4, comment="Very practical shower curtain."),
            Review(user_id=5, product_id=5, rating=3, comment="Chair is okay."),
            Review(user_id=6, product_id=6, rating=5, comment="Perfect for our patio!"),
            Review(user_id=7, product_id=7, rating=4, comment="Nice chandelier."),
            Review(user_id=8, product_id=8, rating=4, comment="Beautiful wall art."),
            Review(user_id=9, product_id=9, rating=5, comment="Great bookshelf."),
            Review(user_id=10, product_id=10, rating=5, comment="Very spacious wardrobe.")
        ]

        db.session.bulk_save_objects(reviews)
        db.session.commit()

if __name__ == "__main__":
    seed_db()

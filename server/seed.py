from app import db, create_app  # Import create_app function and db instance
from models import User, Product, Order, Category, Cart, Review, Address, Payment, Discount
from datetime import datetime, timedelta

# Create an instance of your Flask application
app = create_app()  # Make sure you have a create_app function that initializes your Flask app

# Push an application context
with app.app_context():
    # Drop all existing tables and create new ones
    db.drop_all()
    db.create_all()

    # Seed Users
    user1 = User(
        firstname="John",
        lastname="Doe",
        username="john_doe",
        email="john@example.com",
        password_hash="password123",  # Use the setter method to hash the password
        is_admin=True,
    )

    user2 = User(
        firstname="Jane",
        lastname="Smith",
        username="jane_smith",
        email="jane@example.com",
        password_hash="password123",  # Use the setter method to hash the password
        is_owner=False,
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    # Seed Categories
    category1 = Category(name="Electronics")
    category2 = Category(name="Books")

    db.session.add_all([category1, category2])
    db.session.commit()

    # Seed Products
    product1 = Product(
        name="Smartphone",
        description="Latest model smartphone with advanced features.",
        price=699.99,
        category="Electronics",
        stock=50,
        image_url="http://example.com/smartphone.jpg",
        creator_id=user1.id
    )

    product2 = Product(
        name="Fiction Book",
        description="A gripping novel by a bestselling author.",
        price=19.99,
        category="Books",
        stock=200,
        image_url="http://example.com/book.jpg",
        creator_id=user2.id
    )

    db.session.add_all([product1, product2])
    db.session.commit()

    # Seed Orders
    order1 = Order(
        user_id=user1.id,
        total_amount=719.98,
        status="Pending"
    )

    db.session.add(order1)
    db.session.commit()

    # Seed Order Items
    order_item1 = OrderItem(
        order_id=order1.id,
        product_id=product1.id,
        quantity=1,
        price=699.99
    )

    order_item2 = OrderItem(
        order_id=order1.id,
        product_id=product2.id,
        quantity=1,
        price=19.99
    )

    db.session.add_all([order_item1, order_item2])
    db.session.commit()

    # Seed Carts
    cart1 = Cart(user_id=user1.id)

    db.session.add(cart1)
    db.session.commit()

    # Seed Cart Items
    cart_item1 = CartItem(cart_id=cart1.id, product_id=product1.id, quantity=1)

    db.session.add(cart_item1)
    db.session.commit()

    # Seed Reviews
    review1 = Review(user_id=user1.id, product_id=product1.id, rating=5, comment="Excellent product!")
    review2 = Review(user_id=user2.id, product_id=product2.id, rating=4, comment="Enjoyable read.")

    db.session.add_all([review1, review2])
    db.session.commit()

    # Seed Addresses
    address1 = Address(
        user_id=user1.id,
        street="123 Main St",
        city="Anytown",
        state="Anystate",
        zip_code="12345",
        country="USA"
    )

    db.session.add(address1)
    db.session.commit()

    # Seed Payments
    payment1 = Payment(
        user_id=user1.id,
        order_id=order1.id,
        amount=719.98,
        payment_method="Credit Card",
        status="Completed"
    )

    db.session.add(payment1)
    db.session.commit()

    # Seed Discounts
    discount1 = Discount(
        product_id=product1.id,
        discount_percentage=10.0,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30)
    )

    db.session.add(discount1)
    db.session.commit()

    print("Database seeded successfully.")

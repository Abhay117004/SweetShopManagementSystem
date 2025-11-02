from app import app
from database import db
from models import Sweet, Customer, Order, OrderItem
import os

with app.app_context():
    db_path = 'instance/sweetshop.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Removed old database")

    db.create_all()
    print("✅ Created fresh database")
    sweets = [
        Sweet(name='Chocolate Truffle', description='Rich dark chocolate truffle',
              price=2.50, quantity=100, category='Chocolate'),
        Sweet(name='Strawberry Candy', description='Sweet strawberry flavored candy',
              price=1.50, quantity=150, category='Candy'),
        Sweet(name='Vanilla Cupcake', description='Delicious vanilla cupcake with frosting',
              price=3.00, quantity=50, category='Baked'),
        Sweet(name='Lemon Drops', description='Tangy lemon flavored drops',
              price=1.00, quantity=200, category='Candy'),
        Sweet(name='Caramel Fudge', description='Smooth caramel fudge',
              price=2.00, quantity=80, category='Fudge'),
        Sweet(name='Mint Chocolate', description='Refreshing mint chocolate',
              price=2.25, quantity=120, category='Chocolate'),
    ]

    for sweet in sweets:
        db.session.add(sweet)
    customers = [
        Customer(name='John Doe', email='john@example.com',
                 phone='123-456-7890', address='123 Main St'),
        Customer(name='Jane Smith', email='jane@example.com',
                 phone='234-567-8901', address='456 Oak Ave'),
        Customer(name='Bob Johnson', email='bob@example.com',
                 phone='345-678-9012', address='789 Pine Rd'),
    ]

    for customer in customers:
        db.session.add(customer)

    db.session.commit()

    print("✅ Sample data added successfully!")
    print(f"   - {len(sweets)} sweets")
    print(f"   - {len(customers)} customers")
    print("\n💡 Restart your Flask server for changes to take effect!")

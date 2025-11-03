import os
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# CORS Configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-User-ID"]
    }
})

# Database Configuration
database_uri = os.environ.get('DATABASE_URL_UNPOOLED') or os.environ.get(
    'DATABASE_URL', 'sqlite:///sweetshop.db')
# Fix postgres:// to postgresql:// for SQLAlchemy
if database_uri.startswith('postgres://'):
    database_uri = database_uri.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models


class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(100000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'stock': self.quantity,
            'category': self.category,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'email', name='unique_user_email'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship(
        'OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'total_amount': self.total_amount,
            'total_price': self.total_amount,
            'status': self.status,
            'order_date': self.order_date.isoformat(),
            'items': [item.to_dict() for item in self.order_items]
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey(
        'sweets.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    sweet = db.relationship('Sweet', backref='order_items')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'sweet_id': self.sweet_id,
            'sweet': self.sweet.to_dict() if self.sweet else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }


# Helper functions
def get_user_id():
    """Get user ID from request headers"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        raise ValueError('User ID required')
    return user_id


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            get_user_id()
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
    return decorated_function


# Routes
@app.route('/')
@app.route('/api')
@app.route('/api/')
def index():
    """Welcome page with API information"""
    return jsonify({
        'message': 'Welcome to Sweet Shop Management System API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'sweets': '/api/sweets',
            'customers': '/api/customers',
            'orders': '/api/orders',
            'dashboard': '/api/dashboard/stats'
        },
        'documentation': 'See README.md for full API documentation'
    })


@app.route('/api/health')
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'message': 'Sweet Shop API is running'})


# Sweet Routes
@app.route('/api/sweets', methods=['GET'])
@require_auth
def get_sweets():
    """Get all sweets with optional category filter"""
    user_id = get_user_id()
    category = request.args.get('category')
    query = Sweet.query.filter_by(user_id=user_id)
    if category:
        query = query.filter_by(category=category)
    sweets = query.all()
    return jsonify([sweet.to_dict() for sweet in sweets])


@app.route('/api/sweets/<int:id>', methods=['GET'])
@require_auth
def get_sweet(id):
    """Get a single sweet by ID"""
    user_id = get_user_id()
    sweet = Sweet.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(sweet.to_dict())


@app.route('/api/sweets', methods=['POST'])
@require_auth
def create_sweet():
    """Create a new sweet"""
    user_id = get_user_id()
    data = request.get_json()

    try:
        sweet = Sweet(
            user_id=user_id,
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            quantity=data.get('stock', data.get('quantity', 0)),
            category=data.get('category', ''),
            image_url=data.get('image_url', '')
        )
        db.session.add(sweet)
        db.session.commit()
        return jsonify(sweet.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/sweets/<int:id>', methods=['PUT'])
@require_auth
def update_sweet(id):
    """Update an existing sweet"""
    user_id = get_user_id()
    sweet = Sweet.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()

    try:
        sweet.name = data.get('name', sweet.name)
        sweet.description = data.get('description', sweet.description)
        sweet.price = data.get('price', sweet.price)
        sweet.quantity = data.get(
            'stock', data.get('quantity', sweet.quantity))
        sweet.category = data.get('category', sweet.category)
        sweet.image_url = data.get('image_url', sweet.image_url)

        db.session.commit()
        return jsonify(sweet.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/sweets/<int:id>', methods=['DELETE'])
@require_auth
def delete_sweet(id):
    """Delete a sweet"""
    user_id = get_user_id()
    sweet = Sweet.query.filter_by(id=id, user_id=user_id).first_or_404()

    try:
        order_items = OrderItem.query.filter_by(sweet_id=id).first()
        if order_items:
            return jsonify({'error': 'Cannot delete sweet that is used in orders'}), 400

        db.session.delete(sweet)
        db.session.commit()
        return jsonify({'message': 'Sweet deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# Customer Routes
@app.route('/api/customers', methods=['GET'])
@require_auth
def get_customers():
    """Get all customers"""
    user_id = get_user_id()
    customers = Customer.query.filter_by(user_id=user_id).all()
    return jsonify([customer.to_dict() for customer in customers])


@app.route('/api/customers/<int:id>', methods=['GET'])
@require_auth
def get_customer(id):
    """Get a single customer by ID"""
    user_id = get_user_id()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(customer.to_dict())


@app.route('/api/customers', methods=['POST'])
@require_auth
def create_customer():
    """Create a new customer"""
    user_id = get_user_id()
    data = request.get_json()

    try:
        customer = Customer(
            user_id=user_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/customers/<int:id>', methods=['PUT'])
@require_auth
def update_customer(id):
    """Update an existing customer"""
    user_id = get_user_id()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()

    try:
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)

        db.session.commit()
        return jsonify(customer.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/customers/<int:id>', methods=['DELETE'])
@require_auth
def delete_customer(id):
    """Delete a customer"""
    user_id = get_user_id()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first_or_404()

    try:
        orders = Order.query.filter_by(customer_id=id).first()
        if orders:
            return jsonify({'error': 'Cannot delete customer that has orders'}), 400

        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# Order Routes
@app.route('/api/orders', methods=['GET'])
@require_auth
def get_orders():
    """Get all orders with optional customer filter"""
    user_id = get_user_id()
    customer_id = request.args.get('customer_id')
    query = Order.query.filter_by(user_id=user_id)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    orders = query.all()
    return jsonify([order.to_dict() for order in orders])


@app.route('/api/orders/<int:id>', methods=['GET'])
@require_auth
def get_order(id):
    """Get a single order by ID"""
    user_id = get_user_id()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict())


@app.route('/api/orders', methods=['POST'])
@require_auth
def create_order():
    """Create a new order"""
    user_id = get_user_id()
    data = request.get_json()

    try:
        order = Order(
            user_id=user_id,
            customer_id=data['customer_id'],
            total_amount=0,
            status=data.get('status', 'pending')
        )
        db.session.add(order)
        db.session.flush()

        total = 0
        for item_data in data.get('items', []):
            sweet = Sweet.query.filter_by(
                id=item_data['sweet_id'], user_id=user_id).first()
            if not sweet:
                raise ValueError(
                    f"Sweet with ID {item_data['sweet_id']} not found")

            if sweet.quantity < item_data['quantity']:
                raise ValueError(f"Insufficient stock for {sweet.name}")

            order_item = OrderItem(
                order_id=order.id,
                sweet_id=item_data['sweet_id'],
                quantity=item_data['quantity'],
                price=sweet.price
            )
            db.session.add(order_item)
            sweet.quantity -= item_data['quantity']
            total += sweet.price * item_data['quantity']

        order.total_amount = total
        db.session.commit()

        return jsonify(order.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/orders/<int:id>', methods=['PUT'])
@require_auth
def update_order(id):
    """Update order status"""
    user_id = get_user_id()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()

    try:
        order.status = data.get('status', order.status)
        db.session.commit()
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/orders/<int:id>', methods=['DELETE'])
@require_auth
def delete_order(id):
    """Delete an order and restore inventory"""
    user_id = get_user_id()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()

    try:
        for item in order.order_items:
            sweet = Sweet.query.get(item.sweet_id)
            if sweet:
                sweet.quantity += item.quantity

        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# Dashboard Routes
@app.route('/api/dashboard/stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = get_user_id()
    total_sweets = Sweet.query.filter_by(user_id=user_id).count()
    total_customers = Customer.query.filter_by(user_id=user_id).count()
    total_orders = Order.query.filter_by(user_id=user_id).count()
    pending_orders = Order.query.filter_by(
        user_id=user_id, status='pending').count()

    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.user_id == user_id).scalar() or 0

    return jsonify({
        'total_sweets': total_sweets,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue
    })


@app.route('/api/categories', methods=['GET'])
@require_auth
def get_categories():
    """Get all unique categories"""
    user_id = get_user_id()
    categories = db.session.query(Sweet.category).filter(
        Sweet.user_id == user_id).distinct().all()
    return jsonify([cat[0] for cat in categories if cat[0]])


# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")

        # Migration: Update image_url column to TEXT if it exists as VARCHAR
        try:
            db.session.execute(
                db.text("ALTER TABLE sweets ALTER COLUMN image_url TYPE TEXT"))
            db.session.commit()
            print("Migration: Updated image_url to TEXT type")
        except Exception as migration_error:
            db.session.rollback()
            print(
                f"Migration note (may already be applied): {migration_error}")

    except Exception as e:
        print(f"Error creating tables: {e}")

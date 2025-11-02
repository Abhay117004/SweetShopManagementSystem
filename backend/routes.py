from flask import jsonify, request, Blueprint
from database import db
from models import Sweet, Customer, Order, OrderItem
from sqlalchemy.exc import IntegrityError
from functools import wraps

bp = Blueprint('api', __name__)


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


@bp.route('/', methods=['GET'])
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

# Sweet Routes


@bp.route('/sweets', methods=['GET'])
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


@bp.route('/sweets/<int:id>', methods=['GET'])
@require_auth
def get_sweet(id):
    """Get a single sweet by ID"""
    user_id = get_user_id()
    sweet = Sweet.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(sweet.to_dict())


@bp.route('/sweets', methods=['POST'])
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


@bp.route('/sweets/<int:id>', methods=['PUT'])
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


@bp.route('/sweets/<int:id>', methods=['DELETE'])
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


@bp.route('/customers', methods=['GET'])
@require_auth
def get_customers():
    """Get all customers"""
    user_id = get_user_id()
    customers = Customer.query.filter_by(user_id=user_id).all()
    return jsonify([customer.to_dict() for customer in customers])


@bp.route('/customers/<int:id>', methods=['GET'])
@require_auth
def get_customer(id):
    """Get a single customer by ID"""
    user_id = get_user_id()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(customer.to_dict())


@bp.route('/customers', methods=['POST'])
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


@bp.route('/customers/<int:id>', methods=['PUT'])
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


@bp.route('/customers/<int:id>', methods=['DELETE'])
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


@bp.route('/orders', methods=['GET'])
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


@bp.route('/orders/<int:id>', methods=['GET'])
@require_auth
def get_order(id):
    """Get a single order by ID"""
    user_id = get_user_id()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict())


@bp.route('/orders', methods=['POST'])
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


@bp.route('/orders/<int:id>', methods=['PUT'])
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


@bp.route('/orders/<int:id>', methods=['DELETE'])
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


@bp.route('/dashboard/stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = get_user_id()
    total_sweets = Sweet.query.filter_by(user_id=user_id).count()
    total_customers = Customer.query.filter_by(user_id=user_id).count()
    total_orders = Order.query.filter_by(user_id=user_id).count()
    pending_orders = Order.query.filter_by(
        user_id=user_id, status='pending').count()

    total_revenue = db.session.query(
        db.func.sum(Order.total_amount)).filter(Order.user_id == user_id).scalar() or 0

    return jsonify({
        'total_sweets': total_sweets,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue
    })


@bp.route('/categories', methods=['GET'])
@require_auth
def get_categories():
    """Get all unique categories"""
    user_id = get_user_id()
    categories = db.session.query(Sweet.category).filter(
        Sweet.user_id == user_id).distinct().all()
    return jsonify([cat[0] for cat in categories if cat[0]])


@bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'message': 'Sweet Shop API is running'})

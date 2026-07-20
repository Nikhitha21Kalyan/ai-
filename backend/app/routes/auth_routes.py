from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.utils.auth import hash_password, verify_password, generate_token
from bson.errors import InvalidId

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Create user model
        user_model = User(current_app.db)
        
        # Check if user already exists
        existing_user = user_model.find_by_email(data['email'])
        if existing_user:
            return jsonify({'message': 'User already exists'}), 409
        
        # Hash password and create user
        password_hash = hash_password(data['password'])
        user_id = user_model.create_user(
            email=data['email'],
            password_hash=password_hash,
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data.get('age'),
            gender=data.get('gender')
        )
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing email or password'}), 400
        
        user_model = User(current_app.db)
        user = user_model.find_by_email(data['email'])
        
        if not user or not verify_password(data['password'], user['password_hash']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        token = generate_token(user['_id'], current_app)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/verify', methods=['GET'])
def verify():
    """Verify if a token is valid"""
    try:
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'valid': False}), 401
        
        if not token:
            return jsonify({'valid': False}), 401
        
        from app.utils.auth import verify_token
        user_id = verify_token(token, current_app)
        
        if user_id:
            user_model = User(current_app.db)
            user = user_model.find_by_id(user_id)
            if user:
                return jsonify({
                    'valid': True,
                    'user': {
                        'id': str(user['_id']),
                        'email': user['email'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name']
                    }
                }), 200
        
        return jsonify({'valid': False}), 401
    
    except Exception as e:
        return jsonify({'valid': False, 'message': str(e)}), 500

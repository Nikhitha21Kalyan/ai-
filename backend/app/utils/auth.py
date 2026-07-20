import jwt
import bcrypt
from functools import wraps
from flask import current_app, request, jsonify
from datetime import datetime, timedelta

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=10)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_token(user_id, app):
    """Generate JWT token for a user"""
    payload = {
        'user_id': str(user_id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION']
    }
    token = jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')
    return token

def verify_token(token, app):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid authorization header'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        user_id = verify_token(token, current_app)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated_function

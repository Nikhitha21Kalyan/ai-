from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.utils.auth import token_required

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    """Get user profile"""
    try:
        user_model = User(current_app.db)
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'id': str(user['_id']),
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'age': user.get('age'),
            'gender': user.get('gender'),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(user_id):
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Allowed fields to update
        allowed_fields = ['first_name', 'last_name', 'age', 'gender']
        update_data = {field: data[field] for field in allowed_fields if field in data}
        
        if not update_data:
            return jsonify({'message': 'No valid fields to update'}), 400
        
        user_model = User(current_app.db)
        success = user_model.update_user(user_id, update_data)
        
        if success:
            user = user_model.find_by_id(user_id)
            return jsonify({
                'message': 'Profile updated successfully',
                'user': {
                    'id': str(user['_id']),
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'age': user.get('age'),
                    'gender': user.get('gender')
                }
            }), 200
        
        return jsonify({'message': 'Failed to update profile'}), 400
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_account(current_user_id, user_id):
    """Delete user account (only own account)"""
    try:
        if current_user_id != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        user_model = User(current_app.db)
        success = user_model.delete_user(user_id)
        
        if success:
            return jsonify({'message': 'Account deleted successfully'}), 200
        
        return jsonify({'message': 'Failed to delete account'}), 400
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

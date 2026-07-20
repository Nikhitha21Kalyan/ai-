from flask import Blueprint, request, jsonify, current_app
from app.models.health_record import HealthRecord
from app.utils.auth import token_required

bp = Blueprint('health', __name__, url_prefix='/api/health')

@bp.route('/records', methods=['GET'])
@token_required
def get_records(user_id):
    """Get all health records for a user"""
    try:
        record_type = request.args.get('type')
        
        health_model = HealthRecord(current_app.db)
        records = health_model.get_user_records(user_id, record_type)
        
        # Convert ObjectId to string for JSON serialization
        for record in records:
            record['_id'] = str(record['_id'])
            record['user_id'] = str(record['user_id'])
            if record.get('created_at'):
                record['created_at'] = record['created_at'].isoformat()
            if record.get('updated_at'):
                record['updated_at'] = record['updated_at'].isoformat()
        
        return jsonify({
            'records': records,
            'total': len(records)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/records', methods=['POST'])
@token_required
def create_record(user_id):
    """Create a new health record"""
    try:
        data = request.get_json()
        
        if 'record_type' not in data or 'data' not in data:
            return jsonify({'message': 'Missing required fields'}), 400
        
        health_model = HealthRecord(current_app.db)
        record_id = health_model.create_record(
            user_id=user_id,
            record_type=data['record_type'],
            data=data['data'],
            file_path=data.get('file_path')
        )
        
        return jsonify({
            'message': 'Record created successfully',
            'record_id': record_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/records/<record_id>', methods=['GET'])
@token_required
def get_record(user_id, record_id):
    """Get a specific health record"""
    try:
        health_model = HealthRecord(current_app.db)
        record = health_model.get_record_by_id(record_id)
        
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        # Verify ownership
        if str(record['user_id']) != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        record['_id'] = str(record['_id'])
        record['user_id'] = str(record['user_id'])
        if record.get('created_at'):
            record['created_at'] = record['created_at'].isoformat()
        if record.get('updated_at'):
            record['updated_at'] = record['updated_at'].isoformat()
        
        return jsonify(record), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/records/<record_id>', methods=['PUT'])
@token_required
def update_record(user_id, record_id):
    """Update a health record"""
    try:
        data = request.get_json()
        
        health_model = HealthRecord(current_app.db)
        record = health_model.get_record_by_id(record_id)
        
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        # Verify ownership
        if str(record['user_id']) != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        success = health_model.update_record(record_id, data)
        
        if success:
            return jsonify({'message': 'Record updated successfully'}), 200
        
        return jsonify({'message': 'Failed to update record'}), 400
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/records/<record_id>', methods=['DELETE'])
@token_required
def delete_record(user_id, record_id):
    """Delete a health record"""
    try:
        health_model = HealthRecord(current_app.db)
        record = health_model.get_record_by_id(record_id)
        
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        # Verify ownership
        if str(record['user_id']) != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        success = health_model.delete_record(record_id)
        
        if success:
            return jsonify({'message': 'Record deleted successfully'}), 200
        
        return jsonify({'message': 'Failed to delete record'}), 400
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

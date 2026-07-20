from flask import Blueprint, request, jsonify, current_app
from app.models.health_record import HealthRecord
from app.utils.auth import token_required

bp = Blueprint('report', __name__, url_prefix='/api/reports')

@bp.route('', methods=['GET'])
@token_required
def get_reports(user_id):
    """Get all medical reports"""
    try:
        health_model = HealthRecord(current_app.db)
        reports = health_model.get_user_records(user_id, 'report')
        
        for report in reports:
            report['_id'] = str(report['_id'])
            report['user_id'] = str(report['user_id'])
            if report.get('created_at'):
                report['created_at'] = report['created_at'].isoformat()
        
        return jsonify({'reports': reports}), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('', methods=['POST'])
@token_required
def create_report(user_id):
    """Create a new medical report"""
    try:
        data = request.get_json()
        
        if 'title' not in data or 'content' not in data:
            return jsonify({'message': 'Missing title or content'}), 400
        
        report_data = {
            'title': data['title'],
            'content': data['content'],
            'doctor': data.get('doctor'),
            'diagnosis': data.get('diagnosis'),
            'medication': data.get('medication'),
            'notes': data.get('notes')
        }
        
        health_model = HealthRecord(current_app.db)
        report_id = health_model.create_record(
            user_id=user_id,
            record_type='report',
            data=report_data
        )
        
        return jsonify({
            'message': 'Report created successfully',
            'report_id': report_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<report_id>', methods=['GET'])
@token_required
def get_report(user_id, report_id):
    """Get a specific report"""
    try:
        health_model = HealthRecord(current_app.db)
        report = health_model.get_record_by_id(report_id)
        
        if not report or report.get('record_type') != 'report':
            return jsonify({'message': 'Report not found'}), 404
        
        if str(report['user_id']) != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        report['_id'] = str(report['_id'])
        report['user_id'] = str(report['user_id'])
        if report.get('created_at'):
            report['created_at'] = report['created_at'].isoformat()
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<report_id>', methods=['DELETE'])
@token_required
def delete_report(user_id, report_id):
    """Delete a report"""
    try:
        health_model = HealthRecord(current_app.db)
        report = health_model.get_record_by_id(report_id)
        
        if not report:
            return jsonify({'message': 'Report not found'}), 404
        
        if str(report['user_id']) != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        success = health_model.delete_record(report_id)
        
        if success:
            return jsonify({'message': 'Report deleted successfully'}), 200
        
        return jsonify({'message': 'Failed to delete report'}), 400
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

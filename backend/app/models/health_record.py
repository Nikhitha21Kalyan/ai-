from datetime import datetime
from bson.objectid import ObjectId

class HealthRecord:
    """Health record model"""
    
    collection_name = 'health_records'
    
    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]
    
    def create_record(self, user_id, record_type, data, file_path=None):
        """Create a new health record"""
        record_data = {
            'user_id': ObjectId(user_id),
            'record_type': record_type,  # 'report', 'upload', 'test_result', etc.
            'data': data,
            'file_path': file_path,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(record_data)
        return str(result.inserted_id)
    
    def get_user_records(self, user_id, record_type=None):
        """Get all records for a user"""
        query = {'user_id': ObjectId(user_id)}
        if record_type:
            query['record_type'] = record_type
        return list(self.collection.find(query).sort('created_at', -1))
    
    def get_record_by_id(self, record_id):
        """Get a specific record"""
        try:
            return self.collection.find_one({'_id': ObjectId(record_id)})
        except:
            return None
    
    def update_record(self, record_id, update_data):
        """Update a health record"""
        update_data['updated_at'] = datetime.utcnow()
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(record_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_record(self, record_id):
        """Delete a health record"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(record_id)})
            return result.deleted_count > 0
        except:
            return False

from datetime import datetime
from bson.objectid import ObjectId

class User:
    """User model for healthcare application"""
    
    collection_name = 'users'
    
    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]
    
    def create_user(self, email, password_hash, first_name, last_name, age=None, gender=None):
        """Create a new user"""
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'gender': gender,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        update_data['updated_at'] = datetime.utcnow()
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_user(self, user_id):
        """Delete a user"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

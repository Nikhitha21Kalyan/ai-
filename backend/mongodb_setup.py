"""
MongoDB Quick Setup & Verification
Run this to check MongoDB and create database if needed
"""

import subprocess
import sys
import time
from pathlib import Path

def print_status(status, message):
    """Print colored status message"""
    if status == "✓":
        print(f"✅ {message}")
    elif status == "✗":
        print(f"❌ {message}")
    elif status == "!":
        print(f"⚠️  {message}")
    else:
        print(f"ℹ️  {message}")

def check_mongodb_running():
    """Check if MongoDB is running"""
    print("\n🔍 Checking if MongoDB is running...")
    
    try:
        from pymongo import MongoClient
        
        # Try to connect
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        client.close()
        
        print_status("✓", "MongoDB is running")
        return True
        
    except Exception as e:
        print_status("✗", f"MongoDB is not running: {str(e)}")
        return False

def start_mongodb():
    """Attempt to start MongoDB"""
    print("\n🚀 Attempting to start MongoDB...")
    
    if sys.platform == 'win32':
        print_status("!", "Windows: Starting MongoDB service...")
        try:
            # Try to start MongoDB service
            result = subprocess.run(
                ['net', 'start', 'MongoDB'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 or 'already' in result.stdout.lower():
                print_status("✓", "MongoDB service started/running")
                time.sleep(2)  # Wait for MongoDB to fully start
                return True
            else:
                print_status("!", f"Could not start MongoDB: {result.stdout}")
                print_status("!", "Try manually:")
                print_status("!", "  1. Open Services (services.msc)")
                print_status("!", "  2. Find 'MongoDB Server'")
                print_status("!", "  3. Right-click and start it")
                return False
        except Exception as e:
            print_status("!", f"Error starting MongoDB: {str(e)}")
            return False
    
    elif sys.platform == 'darwin':  # macOS
        print_status("!", "macOS: Starting MongoDB with brew...")
        try:
            subprocess.run(['brew', 'services', 'start', 'mongodb-community'], 
                         check=True, capture_output=True)
            print_status("✓", "MongoDB started")
            time.sleep(2)
            return True
        except Exception as e:
            print_status("!", f"Error: {str(e)}")
            print_status("!", "Run: brew services start mongodb-community")
            return False
    
    else:  # Linux
        print_status("!", "Linux: Starting MongoDB with systemctl...")
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'mongodb'], 
                         check=True, capture_output=True)
            print_status("✓", "MongoDB started")
            time.sleep(2)
            return True
        except Exception as e:
            print_status("!", f"Error: {str(e)}")
            print_status("!", "Run: sudo systemctl start mongodb")
            return False

def create_database():
    """Create healthcare database and collections"""
    print("\n📊 Setting up healthcare database...")
    
    try:
        from pymongo import MongoClient
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client.healthcare
        
        # Create collections with validation
        if 'users' not in db.list_collection_names():
            db.create_collection('users')
            db.users.create_index('email', unique=True)
            print_status("✓", "Created 'users' collection with email index")
        else:
            print_status("!", "'users' collection already exists")
        
        if 'health_records' not in db.list_collection_names():
            db.create_collection('health_records')
            db.health_records.create_index('user_id')
            print_status("✓", "Created 'health_records' collection with user_id index")
        else:
            print_status("!", "'health_records' collection already exists")
        
        # Show statistics
        users_count = db.users.count_documents({})
        records_count = db.health_records.count_documents({})
        
        print_status("i", f"Database statistics:")
        print_status("i", f"  - Users: {users_count}")
        print_status("i", f"  - Health Records: {records_count}")
        
        client.close()
        return True
        
    except Exception as e:
        print_status("✗", f"Failed to create database: {str(e)}")
        return False

def test_connection():
    """Test database connection and operations"""
    print("\n🧪 Testing database connection...")
    
    try:
        from pymongo import MongoClient
        
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        db = client.healthcare
        
        # Test write
        test_doc = {
            'test': True,
            'timestamp': 'test_' + str(time.time())
        }
        
        # Try to insert and delete
        result = db.test_collection.insert_one(test_doc)
        print_status("✓", f"Write test successful (ID: {result.inserted_id})")
        
        # Try to read
        found = db.test_collection.find_one({'_id': result.inserted_id})
        if found:
            print_status("✓", "Read test successful")
        
        # Clean up
        db.test_collection.delete_one({'_id': result.inserted_id})
        print_status("✓", "Delete test successful")
        
        # Drop test collection
        db.drop_collection('test_collection')
        
        client.close()
        return True
        
    except Exception as e:
        print_status("✗", f"Connection test failed: {str(e)}")
        return False

def main():
    """Main verification flow"""
    print("=" * 60)
    print("🗄️  MongoDB Setup & Verification")
    print("=" * 60)
    
    # Check if MongoDB is running
    if not check_mongodb_running():
        # Try to start it
        if not start_mongodb():
            # Check again
            if not check_mongodb_running():
                print("\n" + "=" * 60)
                print("❌ MongoDB could not be started automatically")
                print("\nManual steps:")
                if sys.platform == 'win32':
                    print("  1. Open Command Prompt as Administrator")
                    print("  2. Run: net start MongoDB")
                    print("  Or: Open Services → MongoDB Server → Start")
                elif sys.platform == 'darwin':
                    print("  1. Run: brew services start mongodb-community")
                else:
                    print("  1. Run: sudo systemctl start mongodb")
                print("=" * 60 + "\n")
                return 1
    
    # Create database if needed
    if not create_database():
        print("\n" + "=" * 60)
        print("⚠️  Database creation completed with warnings")
        print("=" * 60 + "\n")
        return 1
    
    # Test connection
    if not test_connection():
        print("\n" + "=" * 60)
        print("⚠️  Connection test failed")
        print("=" * 60 + "\n")
        return 1
    
    # Success
    print("\n" + "=" * 60)
    print("✅ MongoDB is ready!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run backend: python app.py")
    print("  2. Open browser: http://localhost:5000")
    print("  3. Register a new account")
    print("  4. Test upload functionality")
    print("=" * 60 + "\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

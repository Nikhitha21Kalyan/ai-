"""
Verification Script - Check if everything is configured correctly
Run this from the backend directory: python verify_setup.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def print_status(status, message):
    """Print colored status message"""
    if status == "✓":
        print(f"✅ {status} {message}")
    elif status == "✗":
        print(f"❌ {status} {message}")
    elif status == "!":
        print(f"⚠️  {status} {message}")
    else:
        print(f"ℹ️  {status} {message}")

def check_env_file():
    """Check if .env file exists"""
    print("\n📋 Checking Environment Configuration...")
    
    env_path = Path(".env")
    if env_path.exists():
        print_status("✓", ".env file exists")
        
        # Read and display key variables
        with open(env_path, 'r') as f:
            content = f.read()
            if "MONGODB_URI" in content:
                print_status("✓", "MONGODB_URI configured")
            else:
                print_status("✗", "MONGODB_URI not configured")
            
            if "JWT_SECRET" in content:
                print_status("✓", "JWT_SECRET configured")
            else:
                print_status("✗", "JWT_SECRET not configured")
    else:
        print_status("✗", ".env file not found")
        print_status("!", "Copy .env.example to .env and configure it")
        return False
    
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'pymongo': 'PyMongo',
        'jwt': 'PyJWT',
        'bcrypt': 'Bcrypt',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for package_name, display_name in required_packages.items():
        try:
            __import__(package_name)
            print_status("✓", f"{display_name} installed")
        except ImportError:
            print_status("✗", f"{display_name} NOT installed")
            all_installed = False
    
    if not all_installed:
        print_status("!", "Run: pip install -r requirements.txt")
    
    return all_installed

def check_mongodb():
    """Check if MongoDB is running and accessible"""
    print("\n🗄️  Checking MongoDB Connection...")
    
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/healthcare')
        print_status("i", f"Connecting to: {mongodb_uri}")
        
        # Attempt connection
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        print_status("✓", "MongoDB is running and accessible")
        
        # Check database
        db = client.healthcare
        print_status("✓", "Connected to 'healthcare' database")
        
        # Check collections
        collections = db.list_collection_names()
        print_status("i", f"Collections: {collections if collections else 'None yet'}")
        
        if 'users' in collections:
            user_count = db.users.count_documents({})
            print_status("✓", f"'users' collection exists ({user_count} users)")
        else:
            print_status("!", "'users' collection not created yet (will be on first registration)")
        
        if 'health_records' in collections:
            record_count = db.health_records.count_documents({})
            print_status("✓", f"'health_records' collection exists ({record_count} records)")
        else:
            print_status("!", "'health_records' collection not created yet (will be on first upload)")
        
        client.close()
        return True
        
    except Exception as e:
        print_status("✗", f"MongoDB connection failed: {str(e)}")
        print_status("!", "Make sure MongoDB is running:")
        print_status("!", "  Windows: net start MongoDB")
        print_status("!", "  Mac: brew services start mongodb-community")
        print_status("!", "  Linux: sudo systemctl start mongodb")
        return False

def check_app_structure():
    """Check if app structure is correct"""
    print("\n📁 Checking Application Structure...")
    
    required_files = {
        'app.py': 'Flask entry point',
        'config.py': 'Configuration',
        'requirements.txt': 'Dependencies',
        '.env': 'Environment variables',
        'app/__init__.py': 'App factory',
        'app/models/user.py': 'User model',
        'app/models/health_record.py': 'Health record model',
        'app/routes/auth_routes.py': 'Auth endpoints',
        'app/routes/user_routes.py': 'User endpoints',
        'app/routes/health_routes.py': 'Health endpoints',
        'app/routes/report_routes.py': 'Report endpoints',
        'app/utils/auth.py': 'Auth utilities'
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print_status("✓", f"{description} ({file_path})")
        else:
            print_status("✗", f"{description} ({file_path}) MISSING")
            all_exist = False
    
    return all_exist

def check_frontend_files():
    """Check if frontend files are properly configured"""
    print("\n🌐 Checking Frontend Configuration...")
    
    frontend_files = [
        '../js/config.js',
        '../js/api-client.js',
        '../html/login.html',
        '../html/dashboard.html',
        '../html/upload.html',
        '../html/results.html'
    ]
    
    all_exist = True
    for file_path in frontend_files:
        if Path(file_path).exists():
            file_name = Path(file_path).name
            print_status("✓", f"Frontend file exists ({file_name})")
        else:
            print_status("✗", f"Frontend file missing ({file_path})")
            all_exist = False
    
    return all_exist

def test_flask_app():
    """Test if Flask app can be imported"""
    print("\n🚀 Testing Flask Application...")
    
    try:
        from app import create_app
        
        app = create_app('development')
        print_status("✓", "Flask app created successfully")
        
        with app.app_context():
            print_status("✓", "App context created")
            if hasattr(app, 'db'):
                print_status("✓", "MongoDB connection initialized")
                return True
            else:
                print_status("!", "MongoDB not yet initialized")
                return True
        
    except Exception as e:
        print_status("✗", f"Flask app creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🔍 Healthcare Fraud Detection - Setup Verification")
    print("=" * 60)
    
    results = {
        'Environment': check_env_file(),
        'Dependencies': check_dependencies(),
        'MongoDB': check_mongodb(),
        'App Structure': check_app_structure(),
        'Frontend': check_frontend_files(),
        'Flask App': test_flask_app()
    }
    
    print("\n" + "=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Ready to run the application.")
        print("\nNext step: Run 'python app.py' to start the backend")
        print("Then open: http://localhost:5000")
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        print("\nCommon fixes:")
        print("  1. Ensure MongoDB is running: mongosh")
        print("  2. Activate virtual environment: venv\\Scripts\\activate (Windows)")
        print("  3. Install dependencies: pip install -r requirements.txt")
        print("  4. Create .env file from .env.example and configure it")
    
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

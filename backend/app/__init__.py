from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
from config import config

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize MongoDB
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client.healthcare
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import auth_routes, user_routes, health_routes, report_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(health_routes.bp)
    app.register_blueprint(report_routes.bp)
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'API is running'}, 200
    
    return app

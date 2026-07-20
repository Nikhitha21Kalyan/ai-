from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from pymongo import MongoClient
import os
from config import config

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Get the frontend path
    frontend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'html')
    static_path = os.path.join(os.path.dirname(__file__), '..', '..', 'css')
    
    app = Flask(
        __name__,
        static_folder=static_path,
        static_url_path='/css'
    )
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
    
    # Serve static files (CSS, JS)
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        js_path = os.path.join(os.path.dirname(__file__), '..', '..', 'js')
        return send_from_directory(js_path, filename)
    
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        css_path = os.path.join(os.path.dirname(__file__), '..', '..', 'css')
        return send_from_directory(css_path, filename)
    
    # Serve HTML files
    @app.route('/html/<path:filename>')
    def serve_html(filename):
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'html')
        return send_from_directory(html_path, filename)
    
    # Serve index page
    @app.route('/')
    @app.route('/index.html')
    def serve_index():
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'html')
        return send_from_directory(html_path, 'index.html')
    
    # Catch-all for other routes - serve index.html (SPA support)
    @app.route('/<path:path>')
    def catch_all(path):
        if path and '.' in path:
            # It's a file request
            parts = path.split('/')
            if len(parts) == 2:
                folder, filename = parts
                folder_path = os.path.join(os.path.dirname(__file__), '..', '..', folder)
                if os.path.exists(os.path.join(folder_path, filename)):
                    return send_from_directory(folder_path, filename)
        
        # Default to index.html for SPA routing
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'html')
        return send_from_directory(html_path, 'index.html')
    
    return app

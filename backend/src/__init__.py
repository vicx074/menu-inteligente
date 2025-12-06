from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) 
    
    from src.controllers.sales_controller import sales_bp
    
    app.register_blueprint(sales_bp, url_prefix='/api')
    
    return app
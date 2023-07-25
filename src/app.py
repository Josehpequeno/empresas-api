from flask import Flask
from .database import create_table_company

def create_app():
  app = Flask(__name__)

  create_table_company()

  from .controller import companies, api_bp, swagger_ui_blueprint, SWAGGER_URL

  app.register_blueprint(companies)
  app.register_blueprint(api_bp)
  app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

  return app
  

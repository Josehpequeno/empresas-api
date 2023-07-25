from flask import Flask
from .database import create_table_company

def create_app():
  app = Flask(__name__)

  create_table_company()

  from .controller import companies

  app.register_blueprint(companies)

  return app
  

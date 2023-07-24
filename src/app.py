from flask import Flask
from database import create_table_company

app = Flask(__name__)

# app.config.from_pyfile('src/config.py')

create_table_company()

from controller import *

if __name__ == '__main__':
  app.run()
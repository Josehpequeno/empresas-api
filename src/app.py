from flask import Flask
from .companies.database import create_table_company
from flask_restx import Api, Resource, fields, Namespace
from .companies.routes import init_routes


def create_app():
    app = Flask(__name__)
    create_table_company()

    api = Api(
        app, version="1.0", title="Companies API", description="A companies CRUD API"
    )

    init_routes(app, api)

    return app

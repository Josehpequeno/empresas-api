from .controller import (
    swagger_ui_blueprint,
    SWAGGER_URL,
    companies_routes,
    company_routes,
)


def init_routes(app, api):
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    api.add_namespace(companies_routes)
    api.add_namespace(company_routes)

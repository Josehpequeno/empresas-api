from .database import (
    get_db_connection,
    list_companies,
    save_company,
    update_company,
    find_company,
    delete_company,
)
from flask import request, jsonify, Blueprint
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint

companies = Blueprint("companies", __name__)
api_bp = Blueprint('api', __name__)

api = Api(
    companies, version="1.0", title="Companies API", description="A companies CRUD API"
)

company_model_body = api.model(
    "company_body",
    {
        "uuid": fields.String(readonly=True, description="The company identifier"),
        "nomerazao": fields.String(required=True, description="The company nomerazao"),
        "nomefantasia": fields.String(
            required=True, description="The company fantasia"
        ),
        "cnpj": fields.String(required=True, description="The company cnpj"),
        "cnae": fields.String(required=True, description="The company cnae"),
    },
)

company_model = api.model(
    "company_body",
    {
      "company": {
            "uuid": fields.String(readonly=True, description="The company identifier"),
            "nomerazao": fields.String(
                required=True, description="The company nomerazao"
            ),
            "nomefantasia": fields.String(
                required=True, description="The company fantasia"
            ),
            "cnpj": fields.String(required=True, description="The company cnpj"),
            "cnae": fields.String(required=True, description="The company cnae"),
            "created_at": fields.String(
                readonly=True, description="The company created datetime"
            ),
            "updated_at": fields.String(
                readonly=True, description="The company updated datetime"
            ),
        },},
)

companies_model_list = api.model(
    "company_response_list",
    {
        "companies": [{
            "uuid": fields.String(readonly=True, description="The company identifier"),
            "nomerazao": fields.String(
                required=True, description="The company nomerazao"
            ),
            "nomefantasia": fields.String(
                required=True, description="The company fantasia"
            ),
            "cnpj": fields.String(required=True, description="The company cnpj"),
            "cnae": fields.String(required=True, description="The company cnae"),
            "created_at": fields.String(
                readonly=True, description="The company created datetime"
            ),
            "updated_at": fields.String(
                readonly=True, description="The company updated datetime"
            ),
        }],
        "count": fields.Integer(readonly=True, description="The companies count"),
        "start": fields.Integer(readonly=True, description="The companies start"),
        "limit": fields.Integer(readonly=True, description="The companies limit"),
        "sort": fields.String(readonly=True, description="The companies sort selected"),
        "dir": fields.String(readonly=True, description="The companies sort direction"),
    },
)


ns = api.namespace("companies", description="Company operations")


@ns.route("/companies", methods=["GET"])
class Companies(Resource):
    @ns.marshal_list_with(companies_model_list)
    def list():
        start = int(request.args.get("start", default=0))
        limit = request.args.get("limit", default=10)
        sort = request.args.get("sort", default="uuid")
        sort_dir = request.args.get("dir", default="asc").upper()

        if sort not in (
            "uuid",
            "cnpj",
            "nomerazao",
            "nomefantasia",
            "cnae",
            "created_at",
            "updated_at",
        ):
            return jsonify(
                {
                    "error": "Campo selecinado para ordenação inválida. Escolha id, cnpj, nomerazao, nomefantasia ou cnae."
                }
            )

        if sort_dir not in ("ASC", "DESC"):
            return (
                jsonify({"error": 'Ordem de ordenação inválida. Use "asc" ou "desc".'}),
                400,
            )
        companies = list_companies(start, limit, sort, sort_dir)
        response = {
            "count": len(companies),
            "start": start,
            "limit": limit,
            "sort": sort,
            "dir": sort_dir,
            "companies": [
                {
                    "uuid": company["uuid"],
                    "cnpj": company["cnpj"],
                    "nomerazao": company["nomerazao"],
                    "nomefantasia": company["nomefantasia"],
                    "cnae": company["cnae"],
                    "created_at": company["created_at"],
                    "updated_at": company["updated_at"],
                }
                for company in companies
            ],
        }
        return response, 200

@ns.route("/company", methods=["GET", "POST", "PATCH", "DELETE"])
class Companies(Resource):
    @ns.expect(company_model_body)
    @ns.response(201, 'Company created successfully')
    @ns.response(400, 'Conteúdo inválido')
    @ns.response(500, 'Erro interno')
    def post():
        try:
            data = request.get_json()

            cnpj = data.get("cnpj")
            nomerazao = data.get("nomerazao")
            nomefantasia = data.get("nomefantasia")
            cnae = data.get("cnae")

            error_message = []

            if not cnpj:
                error_message.append("cnpj")
            if not nomefantasia:
                error_message.append("nomefantasia")
            if not nomerazao:
                error_message.append("nomerazao")
            if not cnae:
                error_message.append("cnae")

            if len(error_message) > 0:
                raise KeyError()

            save_company(cnpj, nomerazao, nomefantasia, cnae)

            response = {"message": "Empresa criada com sucesso!"}
            return jsonify(response), 201
        except KeyError:
            return (
                jsonify(
                    {
                        "error": f"Conteúdo inválido. Os campos são obrigatórios: {', '.join(error_message)}"
                    }
                ),
                400,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @ns.response(200, 'Company updated successfully')
    @ns.response(400, 'Conteúdo inválido')
    @ns.response(404, 'Empresa não encontrada')
    @ns.response(500, 'Erro interno')
    def patch(company_uuid):
        try:
            data = request.get_json()

            nomefantasia = data.get("nomefantasia")
            cnae = data.get("cnae")

            error_message = []

            if not nomefantasia and not cnae:
                error_message.append("nomefantasia")
                error_message.append("cnae")
                raise KeyError()

            rows_affected = update_company(company_uuid, nomefantasia, cnae)

            if rows_affected == 0:
                response = {"message": "Empresa não encontrada!"}
                return jsonify(response), 404

            response = {"message": "Empresa atualizada com sucesso!"}
            return jsonify(response), 200
        except KeyError:
            return (
                jsonify(
                    {
                        "error": f"Conteúdo inválido. Os campos são obrigatórios: {', '.join(error_message)}"
                    }
                ),
                400,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @ns.response(200, 'Company updated successfully')
    @ns.response(404, 'Empresa não encontrada')
    @ns.response(500, 'Erro interno')
    @ns.marshal_list_with(company_model)
    def get(company_uuid):
        try:
            company = find_company(company_uuid)
            if not company:
                response = {"message": "Empresa não encontrada"}
                return jsonify(response), 404
            response = {
                "company": {
                    "uuid": company["uuid"],
                    "cnpj": company["cnpj"],
                    "nomerazao": company["nomerazao"],
                    "nomefantasia": company["nomefantasia"],
                    "cnae": company["cnae"],
                    "created_at": company["created_at"],
                    "updated_at": company["updated_at"],
                }
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @ns.response(200, 'Company updated successfully')
    @ns.response(404, 'Empresa não encontrada')
    @ns.response(500, 'Erro interno')
    def delete(company_cnpj):
        try:
            rows_affected = delete_company(company_cnpj)
            if rows_affected == 0:
                response = {"message": "Empresa não encontrada!"}
                return jsonify(response), 404
            response = {"message": "Empresa removida com sucesso!"}
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# api.add_namespace(ns)

# Swagger UI Blueprint
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Your API Documentation'
    }
)
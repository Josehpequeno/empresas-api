from .database import (
    get_db_connection,
    list_companies,
    save_company,
    update_company,
    find_company,
    delete_company,
)
from flask import request, Blueprint
from flask_restx import Api, Resource, Namespace, fields, reqparse, marshal_with
from flask_swagger_ui import get_swaggerui_blueprint
from .config import SWAGGER_URL, API_URL


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Your API Documentation"}
)

companies_routes = Namespace("companies", description="Companies operations")

company_routes = Namespace("company", description="Company operations")


company_model_schema = {
    "uuid": fields.String(readonly=True, description="The company identifier"),
    "nomerazao": fields.String(required=True, description="The company nomerazao"),
    "nomefantasia": fields.String(required=True, description="The company fantasia"),
    "cnpj": fields.String(required=True, description="The company cnpj"),
    "cnae": fields.String(required=True, description="The company cnae"),
    "created_at": fields.String(
        readonly=True, description="The company created datetime"
    ),
    "updated_at": fields.String(
        readonly=True, description="The company updated datetime"
    ),
}

company_body_schema = {
    "nomerazao": fields.String(required=True, description="The company nomerazao"),
    "nomefantasia": fields.String(required=True, description="The company fantasia"),
    "cnpj": fields.String(required=True, description="The company cnpj"),
    "cnae": fields.String(required=True, description="The company cnae"),
}

company_message_schema = {
    "message": fields.String(readonly=True, description="Content of message")
}

company_error_schema = {
    "error": fields.String(readonly=True, description="Content of error message")
}


companies_model = companies_routes.model("companies_model", company_model_schema)

companies_list_response_schema = {
    "companies": fields.List(
        fields.Nested(companies_model), description="List of companies"
    ),
    "count": fields.Integer(readonly=True, description="The companies count"),
    "start": fields.Integer(readonly=True, description="The companies start"),
    "limit": fields.Integer(readonly=True, description="The companies limit"),
    "sort": fields.String(readonly=True, description="The companies sort selected"),
    "dir": fields.String(readonly=True, description="The companies sort direction"),
}

companies_list_response = companies_routes.model(
    "companies_response", companies_list_response_schema
)

company_model_body = company_routes.model("company_body", company_body_schema)

company_model = company_routes.model("company_response", company_model_schema)

company_message_model = company_routes.model("company_message", company_message_schema)

company_error_model = company_routes.model("company_error", company_error_schema)


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    "start", type=int, required=False, default=0, help="Start index for pagination"
)
pagination_parser.add_argument(
    "limit", type=int, required=False, default=10, help="Number of items per page"
)
pagination_parser.add_argument(
    "sort", type=str, required=False, default="uuid", help="Selected ordem"
)
pagination_parser.add_argument(
    "dir", type=str, required=False, default="asc", help="Selected ordem direction"
)


@companies_routes.route("/")
class CompaniesController(Resource):
    @companies_routes.doc(
        params={
            "start": "Start index for pagination",
            "limit": "Number of items per page",
            "sort": "Sort field",
            "dir": "Sort direction",
        }
    )
    @companies_routes.response(200, "Success", companies_list_response)
    def get(self):
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
            return {
                "error": "Campo selecinado para ordenação inválida. Escolha id, cnpj, nomerazao, nomefantasia ou cnae."
            }, 400

        if sort_dir not in ("ASC", "DESC"):
            return {"error": 'Ordem de ordenação inválida. Use "asc" ou "desc".'}, 400

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


@company_routes.route("/")
class CompanyController(Resource):
    @company_routes.expect(company_model_body)
    @company_routes.response(201, "Company created successfully", company_message_model)
    @company_routes.response(400, "Conteúdo inválido", company_message_model)
    @company_routes.response(500, "Erro interno", company_error_model)
    def post(self):
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

            return {"message": "Empresa criada com sucesso!"}, 201
        except KeyError:
            return (
                {
                    "error": f"Conteúdo inválido. Os campos são obrigatórios: {', '.join(error_message)}"
                },
                400,
            )
        except Exception as e:
            return {"error": str(e)}, 500


@company_routes.route("/<string:company_uuid>")
class CompanyUuidController(Resource):
    @company_routes.response(200, "Company updated successfully", company_message_model)
    @company_routes.response(400, "Conteúdo inválido", company_message_model)
    @company_routes.response(404, "Empresa não encontrada", company_message_model)
    @company_routes.response(500, "Erro interno", company_error_model)
    def patch(self, company_uuid):
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
                return response, 404

            response = {"message": "Empresa atualizada com sucesso!"}
            return response, 200
        except KeyError:
            return {
                "error": f"Conteúdo inválido. Os campos são obrigatórios: {', '.join(error_message)}"
            }, 400

        except Exception as e:
            return {"error": str(e)}, 500

    @company_routes.response(200, "Company updated successfully", company_model)
    @company_routes.response(404, "Empresa não encontrada", company_message_model)
    @company_routes.response(500, "Erro interno", company_error_model)
    def get(self, company_uuid):
        try:
            company = find_company(company_uuid)
            if not company:
                response = {"message": "Empresa não encontrada"}
                return response, 404
            response = {
                "uuid": company["uuid"],
                "cnpj": company["cnpj"],
                "nomerazao": company["nomerazao"],
                "nomefantasia": company["nomefantasia"],
                "cnae": company["cnae"],
                "created_at": company["created_at"],
                "updated_at": company["updated_at"],
            }
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 500


@company_routes.route("/<string:company_cnpj>")
class CompanyCnpjController(Resource):
    @company_routes.response(200, "Company updated successfully", company_message_model)
    @company_routes.response(404, "Empresa não encontrada", company_message_model)
    @company_routes.response(500, "Erro interno", company_error_model)
    def delete(self, company_cnpj):
        try:
            rows_affected = delete_company(company_cnpj)
            if rows_affected == 0:
                response = {"message": "Empresa não encontrada!"}
                return response, 404
            response = {"message": "Empresa removida com sucesso!"}
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 500

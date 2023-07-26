from .database import (
    get_db_connection,
    list_companies,
    save_company,
    update_company,
    find_company,
    delete_company,
)
from flask import request, Blueprint
from flask_restx import Api, Resource, Namespace, fields, marshal_with
from flask_swagger_ui import get_swaggerui_blueprint
from .config import SWAGGER_URL, API_URL
from .validates import is_valid_cnpj, is_valid_cnae, is_not_empty

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "API Documentation"}
)

companies_routes = Namespace("companies", description="Companies operations")

company_routes = Namespace("company", description="Company operations")


company_schema = {
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

company_body_patch_schema = {
    "nomefantasia": fields.String(required=False, description="The company fantasia"),
    "cnae": fields.String(required=False, description="The company cnae"),
}

message_schema = {
    "message": fields.String(readonly=True, description="Content of message")
}

error_schema = {
    "error": fields.String(readonly=True, description="Content of error message")
}


company_model_for_companies = companies_routes.model("company_model", company_schema)

companies_list_response_schema = {
    "companies": fields.List(
        fields.Nested(company_model_for_companies), description="List of companies"
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

companies_error = companies_routes.model("companies_error", error_schema)

company_body = company_routes.model("company_body", company_body_schema)

company_body_patch = company_routes.model("company_body_pacth", company_body_patch_schema)

company_response = company_routes.model("company_response", company_schema)

company_message = company_routes.model("company_message", message_schema)

company_error = company_routes.model("company_error", error_schema)


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
    @companies_routes.response(200, "Success response", companies_list_response)
    @companies_routes.response(400, "Failure response", companies_error)
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
    @company_routes.expect(company_body)
    @company_routes.response(201, "Success response", company_message)
    @company_routes.response(400, "Failure response", company_error)
    @company_routes.response(500, "Internal error", company_error)
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

            if not is_valid_cnpj(cnpj):
                return {"message": "cnpj inválido"}, 400
            if not is_valid_cnae(cnae):
                return {"message": "cnae inválido"}, 400

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
    @company_routes.response(200, "Success response", company_response)
    @company_routes.response(404, "Failure response. Not Found", company_error)
    @company_routes.response(500, "Internal error", company_error)
    def get(self, company_uuid):
        try:
            company = find_company(company_uuid)
            if not company:
                response = {"error": "Empresa não encontrada"}
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

    @company_routes.expect(company_body_patch)
    @company_routes.response(200, "Success response", company_message)
    @company_routes.response(400, "Failure response. Invalid content", company_error)
    @company_routes.response(404, "Failure response. Not Found", company_error)
    @company_routes.response(500, "Internal error", company_error)
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

            if (cnae is not None) and (not is_valid_cnae(cnae)):
                return {"message": "cnae inválido"}, 400
            if (nomefantasia is not None) and (not is_not_empty(nomefantasia)):
                return {"message": "nomefantasia inválido"}, 400

            rows_affected = update_company(company_uuid, nomefantasia, cnae)

            if rows_affected == 0:
                response = {"error": "Empresa não encontrada!"}
                return response, 404

            response = {"message": "Empresa atualizada com sucesso!"}
            return response, 200
        except KeyError:
            return {
                "error": f"Conteúdo inválido. Deve conter pelo menos um dos campos: {', '.join(error_message)}"
            }, 400

        except Exception as e:
            return {"error": str(e)}, 500


# path para passar os formatos de cnpj com /
@company_routes.route("/<path:company_cnpj>")
class CompanyCnpjController(Resource):
    @company_routes.response(200, "Success response", company_message)
    @company_routes.response(404, "Failure response. Not Found", company_error)
    @company_routes.response(500, "Internal error", company_error)
    def delete(self, company_cnpj):
        try:
            if not is_valid_cnpj(company_cnpj):
                return {"message": "cnpj inválido"}, 400
            rows_affected = delete_company(company_cnpj)
            if rows_affected == 0:
                response = {"error": "Empresa não encontrada!"}
                return response, 404
            response = {"message": "Empresa removida com sucesso!"}
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 500

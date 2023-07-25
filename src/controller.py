from .database import get_db_connection, list_companies, save_company
from flask import request, jsonify, Blueprint

companies = Blueprint("companies",__name__)

@companies.route("/companies", methods=['GET'])
def list():
    start = int(request.args.get('start', default=0))
    limit = request.args.get('limit', default=10)
    sort = request.args.get('sort', default='uuid')
    sort_dir = request.args.get('dir', default='asc').upper()
    
    if sort not in ('uuid', 'cnpj', 'nomerazao', 'nomefantasia', 'cnae', 'created_at', 'updated_at'):
        return jsonify({'error': 'Campo selecinado para ordenação inválida. Escolha id, cnpj, nomerazao, nomefantasia ou cnae.'})
    
    if sort_dir not in ('ASC', 'DESC'):
        return jsonify({'error': 'Ordem de ordenação inválida. Use "asc" ou "desc".'}), 400
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
                "updated_at": company["updated_at"]
            }
            for company in companies
        ],
    }
    return response, 200


@companies.route("/create_company", methods=["POST"])
def create_company():
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

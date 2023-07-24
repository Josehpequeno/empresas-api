from app import app
from database import get_db_connection, list_companys, save_company
from flask import request, jsonify


@app.route("/companys")
def list():
    companys = list_companys()
    print("companys:", companys)
    response = {
        "companys": [
            {
                "id": company["id"],
                "cnpj": company["cnpj"],
                "nomerazao": company["nomerazao"],
                "nomefantasia": company["nomefantasia"],
                "cnae": company["cnae"]
            }
            for company in companys
        ]
    }
    return response, 200


@app.route("/create_company", methods=["POST"])
def create_company():
    try:
        data = request.get_json()

        cnpj = data["cnpj"]
        nomerazao = data["nomerazao"]
        nomefantasia = data["nomefantasia"]
        cnae = data["cnae"]

        save_company(cnpj, nomerazao, nomefantasia, cnae)

        response = {"message": "Empresa criada com sucesso!"}
        return jsonify(response), 201
    except KeyError:
        return (
            jsonify(
                {
                    "error": "Conteúdo inválido. Veja se os campos cnpj, nomerazao, nomefantasia e cnae foram preenchidos."
                }
            ),
            400,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

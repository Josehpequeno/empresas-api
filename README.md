# Projeto de Gestão de Empresas

Este é um projeto de API para gestão de empresas, desenvolvido em Python com o framework Flask e Flask-RESTx. A API permite realizar operações CRUD (Create, Read, Update e Delete) em empresas, além de fornecer funcionalidades de paginação e ordenação dos resultados.

## Requisitos

- Python 3.6 ou superior
- Flask
- Flask-RESTx
- Flask-Swagger-UI

## Instalação

1. Clone o repositório para sua máquina local:

```
git clone https://github.com/Josehpequeno/teste-backEnd-python.git
```

2. Acesse o diretório do projeto:

```
cd teste-backEnd-python
```

3. Crie um ambiente virtual para o projeto:

```
python -m venv .
```

4. Ative o ambiente virtual:

- No Windows:

```
Scripts\activate
```

- No Linux/macOS:

```
source bin/activate
```

5. Instale as dependências do projeto usando o pip:

```
pip install -r requirements.txt
```

6. Configure as variáveis de ambiente:

- No Windows:

```
set FLASK_APP=src/app.py
set FLASK_ENV=Development
set FLASK_DEBUG=True
```

- No Linux/macOS:

```
export FLASK_APP=src/app.py
export FLASK_ENV=Development
export FLASK_DEBUG=True
```

## Executando a API

Para executar a API, utilize o seguinte comando:

```
flask run
```

A API será executada localmente em `http://localhost:5000/`.

## Documentação

A documentação da API pode ser acessada através da interface do Swagger UI, que estará disponível em `http://localhost:5000/swagger`. Nessa interface, você encontrará todas as rotas disponíveis, seus parâmetros, respostas e exemplos de uso.

## Rotas

A API oferece as seguintes rotas:

### GET /companies

- Descrição: Retorna uma lista de empresas com opções de paginação e ordenação.
- Parâmetros de consulta:
  - `start` (opcional): Índice de início para paginação.
  - `limit` (opcional): Número de itens por página.
  - `sort` (opcional): Campo para ordenação.
  - `dir` (opcional): Direção da ordenação (ascendente ou descendente).

### POST /company

- Descrição: Cria uma nova empresa.
- Corpo da requisição:
  - `nomerazao` (obrigatório): Nome ou razão social da empresa.
  - `nomefantasia` (obrigatório): Nome fantasia da empresa.
  - `cnpj` (obrigatório): CNPJ da empresa (no formato 00000000000000).
  - `cnae` (obrigatório): CNAE da empresa.

### GET /company/<string:company_uuid>

- Descrição: Retorna os detalhes de uma empresa específica.
- Parâmetros de rota:
  - `company_uuid` (obrigatório): UUID da empresa.

### PATCH /company/<string:company_uuid>

- Descrição: Atualiza os dados de uma empresa específica.
- Parâmetros de rota:
  - `company_uuid` (obrigatório): UUID da empresa.
- Corpo da requisição:
  - `nomefantasia` (opcional): Novo nome fantasia da empresa.
  - `cnae` (opcional): Novo CNAE da empresa.

### DELETE /company/<path:company_cnpj>

- Descrição: Remove uma empresa com base no CNPJ informado.
- Parâmetros de rota:
  - `company_cnpj` (obrigatório): CNPJ da empresa (nos formatos 00000000000, 00000000000000, 000.000.000-00, 00.000.000/0000-00, 000000000-00 ou 00000000/0000-00).

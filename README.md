# teste-backEnd-python

### Comandos até agora
```shell

python -m venv .

source bin/activate

export FLASK_APP=src/app.py

export FLASK_ENV=Development

export FLASK_DEBUG=True

flask run

```

### Tarefas 
[x] Criar um endpoint para cadastrar uma nova empresa com os campos obrigatórios: CNPJ, Nome Razão, Nome Fantasia e CNAE.

[x] Implementar um endpoint para editar um cadastro de empresa existente, permitindo alterar apenas os campos Nome Fantasia e CNAE.// uuid

[x] Desenvolver um endpoint para remover um cadastro de empresa existente com base no CNPJ.

[x] Criar um endpoint de listagem de empresas, com suporte à paginação, ordenação e limite de registros por página.

[x] Os dados das empresas podem ser armazenados em memória (em uma lista ou dicionário) ou em um banco de dados de sua escolha (como SQLite, PostgreSQL, etc.).

[x] uuid4

[x] validação 

[x] swagger

[x] encontrar empresa pelo uuid

#### opcional
[x] validação cnpj e cnae
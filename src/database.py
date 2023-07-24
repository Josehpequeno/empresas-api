import sqlite3


class InsertCompanyError(Exception):
    pass


def get_db_connection():
    conn = sqlite3.connect("companys.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table_company():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_company_table = """ 
    CREATE TABLE IF NOT EXISTS companys (
            id INTEGER PRIMARY KEY,
            cnpj TEXT NOT NULL,
            nomerazao TEXT NOT NULL,
            nomefantasia TEXT NOT NULL,
            cnae TEXT NOT NULL
        )  
  """

    cursor.execute(create_company_table)

    conn.commit()
    conn.close()


def list_companys():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companys")
    companys = cursor.fetchall()
    conn.close()
    return companys


def save_company(cnpj, nomerazao, nomefantasia, cnae):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO companys (cnpj, nomerazao, nomefantasia, cnae) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (cnpj, nomerazao, nomefantasia, cnae))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        conn.rollback()

        raise InsertCompanyError(
            "Erro ocorreu durante o registro da empresa: " + str(e)
        )

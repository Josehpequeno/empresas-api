import sqlite3
from datetime import datetime
import uuid


class InsertCompanyError(Exception):
    pass


def get_db_connection():
    conn = sqlite3.connect("companies.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table_company():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_company_table = f""" 
    CREATE TABLE IF NOT EXISTS companies (
            uuid VARCHAR(36) PRIMARY KEY,
            cnpj TEXT NOT NULL,
            nomerazao TEXT NOT NULL,
            nomefantasia TEXT NOT NULL,
            cnae TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL 
        )  
  """

    cursor.execute(create_company_table)

    conn.commit()
    conn.close()


def list_companies(start, limit, sort, sort_dir):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM companies ORDER BY {sort} {sort_dir}"

    if limit is not None:
        query += f" LIMIT {int(limit)} OFFSET {start}"

    cursor.execute(query)
    companies = cursor.fetchall()
    conn.close()
    return companies


def save_company(cnpj, nomerazao, nomefantasia, cnae):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO companies (uuid, cnpj, nomerazao, nomefantasia, cnae, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(
            query,
            (
                str(uuid.uuid4()),
                cnpj,
                nomerazao,
                nomefantasia,
                cnae,
                datetime.now(),
                datetime.now(),
            ),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        conn.rollback()
        raise InsertCompanyError(
            "Erro ocorreu durante o registro da empresa: " + str(e)
        )


def update_company(uuid, nomefantasia, cnae):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE companies SET "
        if nomefantasia is not None:
            query += f"nomefantasia = '{nomefantasia}', "
        if cnae is not None:
            query += f"cnae = '{cnae}', "
        query += f"updated_at = '{datetime.now()}' WHERE uuid = '{uuid}'"
        cursor.execute(query)
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected
    except sqlite3.Error as e:
        conn.rollback()
        raise InsertCompanyError(
            "Erro ocorreu durante a atualização da empresa: " + str(e)
        )


def find_company(uuid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM companies WHERE uuid = '{uuid}'"
        cursor.execute(query)
        company = cursor.fetchone()
        conn.commit()
        conn.close()
        return company
    except sqlite3.Error as e:
        conn.rollback()
        raise InsertCompanyError("Erro ao encontrar empresa: " + str(e))


def delete_company(cnpj):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM companies WHERE cnpj = '{cnpj}'"
        cursor.execute(query)
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected
    except sqlite3.Error as e:
        conn.rollback()
        raise InsertCompanyError("Erro ao deletar empresa: " + str(e))

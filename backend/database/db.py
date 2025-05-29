usuarios_db = {}
festas_db = {}
fornecedores_db = {}

def get_all_dbs():
    return {
        "usuarios": usuarios_db,
        "festas": festas_db,
        "fornecedores": fornecedores_db
    }

# =============================
# 📦 Bibliotecas
# =============================
import sqlite3
import json

# =============================
# 📂 Inicialização do Banco de Dados (SQLite)
# =============================
def init_db(DB_PATH):
    # 🔌 Conexão com o Banco
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 🏗️ Criação das Tabelas
    c.execute('''
      CREATE TABLE IF NOT EXISTS tb_empresa (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        missao TEXT,
        visao TEXT,
        valores TEXT
      )
    ''')
    c.execute('''
      CREATE TABLE IF NOT EXISTS tb_beneficios (
        id INTEGER PRIMARY KEY,
        descricao TEXT
      )
    ''')
    # ⚙️ Dados padrão
    c.execute('SELECT COUNT(*) FROM tb_empresa')
    if c.fetchone()[0] == 0:
        default = {
            "nome": "Acme Corporation",
            "missao": "Nossa missão é inovar.",
            "visao": "Ser referência em ajudar as pessoas.",
            "valores": json.dumps(["Colaboração", "Transparência", "Excelência"])
        }
        c.execute(
            '''INSERT INTO tb_empresa (nome, missao, visao, valores)
               VALUES (?,?,?,?)''',
            (default["nome"], default["missao"], default["visao"], default["valores"])
        )
        for b in ["Vale-refeição", "Plano de Saúde", "GymPass", "PLR"]:
            c.execute(
                'INSERT INTO tb_beneficios(descricao) VALUES (?)',
                (b,)
            )
    conn.commit()
    conn.close()

# =============================
# 📑 Funções de Acesso e Modificação
# =============================
def get_company(DB_PATH):
    # ▶️ Recupera informações da empresa e benefícios
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM tb_empresa LIMIT 1')
    row = dict(c.fetchone())
    row["valores"] = json.loads(row["valores"])
    c.execute('SELECT descricao FROM tb_beneficios')
    row["beneficios"] = [r["descricao"] for r in c.fetchall()]
    conn.close()
    return row

def update_company(DB_PATH, nome, missao, visao, valores):
    # 🔄 Atualiza os dados principais da empresa
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''UPDATE tb_empresa
           SET nome=?, missao=?, visao=?, valores=?
           WHERE id=1''',
        (nome, missao, visao, json.dumps(valores))
    )
    conn.commit()
    conn.close()

def add_benefit(DB_PATH, desc):
    # ➕ Adiciona um novo benefício
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO tb_beneficios(descricao) VALUES (?)',
        (desc,)
    )
    conn.commit()
    conn.close()

def remove_benefit(DB_PATH, desc):
    # ➖ Remove um benefício existente
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'DELETE FROM tb_beneficios WHERE descricao=?',
        (desc,)
    )
    conn.commit()
    conn.close()

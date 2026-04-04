import sqlite3
import os


conexao = sqlite3.connect('banco.db')

cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

criar_tabela_funcionarios = '''CREATE TABLE IF NOT EXISTS
funcionarios 
(
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT,
    email TEXT,
    senha TEXT,
    telefone INTEGER,
    cpf TEXT NOT NULL UNIQUE    
)'''

cursor.execute(criar_tabela_funcionarios)



#==================================================================================================================
create_empresas = '''CREATE TABLE IF NOT EXISTS
empresas
(
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT,
    endereco TEXT,
    email TEXT,
    senha TEXT,
    telefone INTEGER,
    cnpj TEXT NOT NULL UNIQUE
)'''
cursor.execute(create_empresas)



#==================================================================================================================
create_competencias = ''' CREATE TABLE IF NOT EXISTS
competencias
(
    id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)'''
cursor.execute(create_competencias)



#==================================================================================================================


create_vagas = ''' CREATE TABLE IF NOT EXISTS
vagas
(
    id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descricao TEXT,
    salario REAL,
    id_empresa INTEGER,
    id_competencia INTEGER,
    FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia),
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
)'''

cursor.execute(create_vagas)





create_func_comp = ''' CREATE TABLE IF NOT EXISTS funcionario_competencias (
    id_funcionario INTEGER,
    id_competencia INTEGER,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario),
    FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia)
)'''



cursor.execute(create_func_comp)



conexao.commit() # ISSO É O MAIS IMPORTANTE! Sem isso, o banco fica vazio.
conexao.close()
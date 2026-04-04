import sqlite3
import os

conexao = sqlite3.connect('banco.db')


cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS contas_bancarias (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               titular TEXT NOT NULL,
               saldo FLOAT NOT NULL,
               cpf TEXT NOT NULL UNIQUE
               )""")

#cursor.execute("""INSERT INTO contas_bancarias
#               (titular, saldo,cpf) VALUES
#               ('Pedro', 500, '123.456.789-10')""")


#cursor.execute(""" SELECT * FROM contas_bancarias""")
#contas = cursor.fetchall()
#print(contas)
#for conta in contas:
#    id, titular, saldo, cpf = conta
#    print(f"""
#        id: {id} 
#        titular: {titular}
#        saldo: {saldo}
#        cpf: {cpf}""")
#    print("\n")

cursor.execute("""SELECT titular, saldo FROM contas_bancarias""")
contas = cursor.fetchall()
for conta in contas:
    titular, saldo = conta
    print(f"""
        titular: {titular}
        saldo: {saldo}
    """)


cursor.execute("""SELECT titular, saldo FROM contas_bancarias WHERE id = 1 """)
contas = cursor.fetchall()
for conta in contas:
    titular, saldo = conta
    print(f"""
        titular: {titular}
        saldo: {saldo}
    """)
cursor.execute("""UPDATE contas_bancarias SET saldo = 199 WHERE id = 1""")

cursor.execute("DELETE FROM contas_bancarias WHERE id = 1")


conexao.commit()


import sqlite3

class DadoScores:
    def __init__(self):
        self.conectar()
        self.criaTabela()
    
    def conectar(self):
        self.conn = sqlite3.connect('scores.db')
        self.cursor = self.conn.cursor()
    
    def criaTabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores (nome TEXT, pontos INTEGER, data TEXT)''')
        self.conn.commit()
    
    def salvarScores(self, nome, pontos):
        self.cursor.execute("INSERT INTO scores (nome, pontos) VALUES (?, ?)", (nome, pontos))
        self.cursor.execute("SELECT rowid, pontos FROM scores ORDER BY pontos DESC")
        todos_scores = self.cursor.fetchall()
        
        if len(todos_scores) > 10:
            ids_manter = [row[0] for row in todos_scores[:10]]
            placeholders = ','.join(['?'] * len(ids_manter))
            self.cursor.execute(f"DELETE FROM scores WHERE rowid NOT IN ({placeholders})", ids_manter)
        
        self.conn.commit()
    
    def topScores(self, limite=10):
        self.cursor.execute("SELECT nome, pontos FROM scores ORDER BY pontos DESC LIMIT ?", (limite,))
        resultados = self.cursor.fetchall()
        return resultados
    
    def fechar(self):
        self.conn.close()
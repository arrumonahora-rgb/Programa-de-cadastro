import sys
from PySide6 import QtWidgets, QtUiTools, QtCore
import mysql.connector

# Conexão direta
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="cadastro_produtos"
)

def abrir_lista():
    janela_lista.show()

def inserir():
    # Coleta de dados
    produto = window.txtProduto.text()
    preco = window.txtPreco.text()
    estoque = window.txtEstoque.text()
    
    # Execução no Banco de Dados
    cursor = conexao.cursor()
    comando_sql = "INSERT INTO produtos (produto, preco, estoque) VALUES (%s, %s, %s)"
    dados = (str(produto), str(preco), str(estoque))
    cursor.execute(comando_sql, dados)
    conexao.commit()
    
    # Limpa os campos
    window.txtProduto.clear()
    window.txtPreco.clear()
    window.txtEstoque.clear()

# Configuração da Interface
app = QtWidgets.QApplication(sys.argv)
loader = QtUiTools.QUiLoader()

# Carregar o arquivo do formulário
file1 = QtCore.QFile("formulario.ui")
file1.open(QtCore.QFile.ReadOnly)
window = loader.load(file1)
file1.close()

# Carregar o arquivo da lista (em uma variável diferente para não sobrescrever)
file2 = QtCore.QFile("lista.ui")
file2.open(QtCore.QFile.ReadOnly)
janela_lista = loader.load(file2)
file2.close()

# Conectar os eventos
window.btnCadastrar.clicked.connect(inserir)
window.btnRelatorio.clicked.connect(abrir_lista)

# Iniciar o sistema
window.show()
sys.exit(app.exec())
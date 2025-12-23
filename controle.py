import sys
from PySide6 import QtWidgets, QtUiTools, QtCore
import mysql.connector

# Conexão
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="cadastro_produtos"
)

# Variável global
numero_id = 0

# Função editar dados
def editar():
    global numero_id
    linha_selecionada = janela_lista.tableWidget.currentRow() 
    
    valor_id = janela_lista.tableWidget.item(linha_selecionada, 0).text()    
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = %s', (valor_id,))
    leitura_banco = cursor.fetchall()    
    cursor.close() 
    
    janela_editar.show()
    numero_id = valor_id
    
    # Preenche os campos de texto (Body direto)
    janela_editar.txtalterarId.setText(str(leitura_banco[0][0]))
    janela_editar.txtalterarProd.setText(str(leitura_banco[0][1]))
    janela_editar.txtalterarPreco.setText(str(leitura_banco[0][2]))
    janela_editar.txtalterarEstoque.setText(str(leitura_banco[0][3]))    
            
# Atualizar dados
def salvar_dados():
    global numero_id 
    
    id_produto = janela_editar.txtalterarId.text()
    nome = janela_editar.txtalterarProd.text()
    preco = janela_editar.txtalterarPreco.text()
    estoque = janela_editar.txtalterarEstoque.text()    
    
    cursor = conexao.cursor()
    comando_sql = "UPDATE produtos SET produto = %s, preco = %s, estoque = %s WHERE id = %s"
    cursor.execute(comando_sql, (nome, preco, estoque, id_produto))
    
    conexao.commit()
    cursor.close()
    
    janela_editar.close()
    janela_lista.close()
    window.show() 
    
    abrir_lista() 
    numero_id = 0

# Função abrir lista
def abrir_lista():
    janela_lista.show()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    leitura_banco = cursor.fetchall()    
    
    janela_lista.tableWidget.setRowCount(len(leitura_banco)) 
    janela_lista.tableWidget.setColumnCount(4)    
    for i in range(len(leitura_banco)):
        for j in range(4):
            janela_lista.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(leitura_banco[i][j])))
    cursor.close()

# Função inserir dados
def inserir():
    produto = window.txtProduto.text()
    preco = window.txtPreco.text()
    estoque = window.txtEstoque.text()    
    
    cursor = conexao.cursor()
    comando_sql = "INSERT INTO produtos (produto, preco, estoque) VALUES (%s, %s, %s)"
    dados = (str(produto), str(preco), str(estoque))
    cursor.execute(comando_sql, dados)
    conexao.commit() 
    cursor.close()
    
    window.txtProduto.clear()
    window.txtPreco.clear()
    window.txtEstoque.clear()

# Configuração da Interface
app = QtWidgets.QApplication(sys.argv)
loader = QtUiTools.QUiLoader()

window = loader.load("formulario.ui")
janela_lista = loader.load("lista.ui")
janela_editar = loader.load("editar.ui")

# Eventos
window.btnCadastrar.clicked.connect(inserir)
window.btnRelatorio.clicked.connect(abrir_lista)
janela_lista.btnAlterar.clicked.connect(editar)
janela_editar.btnSalvarDados.clicked.connect(salvar_dados)

window.show()
sys.exit(app.exec())
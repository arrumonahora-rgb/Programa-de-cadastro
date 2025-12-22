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

# Funções salvar dados
def salvar_dados():
    # Coleta os novos dados da tabela de edição
    id_produto = janela_editar.tableWidget.item(0, 0).text()
    nome = janela_editar.tableWidget.item(0, 1).text()
    preco = janela_editar.tableWidget.item(0, 2).text()
    estoque = janela_editar.tableWidget.item(0, 3).text()    
    
    cursor = conexao.cursor()
    comando_sql = "UPDATE produtos SET produto = %s, preco = %s, estoque = %s WHERE id = %s"
    cursor.execute(comando_sql, (nome, preco, estoque, id_produto))
    conexao.commit()
    
    janela_editar.close()
    abrir_lista() 

# Função editar dados
def editar():
    linha_selecionada = janela_lista.tableWidget.currentRow() 
    
    if linha_selecionada == -1:
        return
    valor_id = janela_lista.tableWidget.item(linha_selecionada, 0).text()    
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = %s', (valor_id,))
    leitura_banco = cursor.fetchall()    
    janela_editar.show()    
    
    janela_editar.txtalterarId.setText(str(leitura_banco[0][0]))
    janela_editar.txtalterarProd.setText(str(leitura_banco[0][1]))
    janela_editar.txtalterarPreco.setText(str(leitura_banco[0][2]))
    janela_editar.txtalterarEstoque.setText(str(leitura_banco[0][3]))   
    
    print(dir(janela_editar))
    
    janela_editar.tableWidget.setRowCount(len(leitura_banco)) 
    janela_editar.tableWidget.setColumnCount(4)    
    
    for i in range(len(leitura_banco)):
        for j in range(4):
            item = QtWidgets.QTableWidgetItem(str(leitura_banco[i][j]))
            janela_editar.tableWidget.setItem(i, j, item)
            
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

# Função inserir dados
def inserir():
    produto = window.txtProduto.text()
    preco = window.txtPreco.text()
    estoque = window.txtEstoque.text()    
    if not produto: return 
    cursor = conexao.cursor()
    comando_sql = "INSERT INTO produtos (produto, preco, estoque) VALUES (%s, %s, %s)"
    dados = (str(produto), str(preco), str(estoque))
    cursor.execute(comando_sql, dados)
    conexao.commit()    
    window.txtProduto.clear()
    window.txtPreco.clear()
    window.txtEstoque.clear()

# Configuração da Interface
app = QtWidgets.QApplication(sys.argv)
loader = QtUiTools.QUiLoader()

# Carregamento das Janelas
window = loader.load("formulario.ui")
janela_lista = loader.load("lista.ui")
janela_editar = loader.load("editar.ui")

# Eventos dos Botões
window.btnCadastrar.clicked.connect(inserir)
window.btnRelatorio.clicked.connect(abrir_lista)
janela_lista.btnAlterar.clicked.connect(editar)

# APP EXEC
window.show()
sys.exit(app.exec())
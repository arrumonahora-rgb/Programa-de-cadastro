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

# Variável global definida no escopo principal
numero_id = 0

# Função editar dados
def editar():
    global numero_id
    linha_selecionada = janela_lista.tableWidget.currentRow() 
    
    if linha_selecionada == -1:
        return
    
    valor_id = janela_lista.tableWidget.item(linha_selecionada, 0).text()    
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = %s', (valor_id,))
    leitura_banco = cursor.fetchall()    
    cursor.close() 
    
    if not leitura_banco:
        return

    janela_editar.show()
    numero_id = valor_id
    
    # Preenche os campos de texto
    janela_editar.txtalterarId.setText(str(leitura_banco[0][0]))
    janela_editar.txtalterarProd.setText(str(leitura_banco[0][1]))
    janela_editar.txtalterarPreco.setText(str(leitura_banco[0][2]))
    janela_editar.txtalterarEstoque.setText(str(leitura_banco[0][3]))    
    
    # Preenche a tabela interna da janela de edição
    janela_editar.tableWidget.setRowCount(len(leitura_banco)) 
    janela_editar.tableWidget.setColumnCount(4)    
    
    for i in range(len(leitura_banco)):
        for j in range(4):
            item = QtWidgets.QTableWidgetItem(str(leitura_banco[i][j]))
            janela_editar.tableWidget.setItem(i, j, item)
            
# Atualizar dados
def salvar_dados():
    global numero_id 
    
    # Coleta os dados atualizados dos campos de texto
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
    abrir_lista() # Atualiza a lista principal após salvar
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
    
    if not produto: 
        return 
        
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

# Carregamento das Janelas
window = loader.load("formulario.ui")
janela_lista = loader.load("lista.ui")
janela_editar = loader.load("editar.ui")

# Eventos dos Botões
window.btnCadastrar.clicked.connect(inserir)
window.btnRelatorio.clicked.connect(abrir_lista)
janela_lista.btnAlterar.clicked.connect(editar)

# Conectando o botão de salvar da janela de edição
# IMPORTANTE: Verifique se o nome do objeto no Qt Designer é exatamente 'btnSalvarDados'
try:
    janela_editar.btnSalvarDados.clicked.connect(salvar_dados)
except AttributeError:
    print("Erro: O botão 'btnSalvarDados' não foi encontrado em editar.ui")

# APP EXEC
window.show()
sys.exit(app.exec())
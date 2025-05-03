import mysql.connector  #Importa a biblioteca para conexão com banco de dados MySQL
import uuid #Biblioteca para criar códigos únicos

def registrar_receita_pdf(paciente_id, caminho_pdf, config): #Função para enviar a receita para o banco de dados

    try:
        #Estabelecimento de conexão com o banco de dados usando as configurações passadas (estarão no main.py as configs)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        #Abre o arquivo PDF no caminho especificado em modo binário (r= read b= binary)
        with open(caminho_pdf, "rb") as file:
            pdf_data = file.read()  #Lê o conteúdo binário do PDF

        #Executa um comando SQL para inserir o ID do paciente e o PDF na tabela "receitas"
        cursor.execute("""
            INSERT INTO receitas (paciente_id, arquivo_pdf)
            VALUES (%s, %s)
        """, (paciente_id, pdf_data))

        #Confirma (commita) a transação no banco de dados
        conn.commit()

        #Retorna uma mensagem de sucesso
        return f"Receita para o paciente com ID {paciente_id} registrada com sucesso!"

    #Captura erros específicos do MySQL e retorna uma mensagem com o erro
    except mysql.connector.Error as err:
        return f"Erro de banco de dados: {err}"

    #Captura outros tipos de erros e retorna uma mensagem com o erro
    except Exception as e:
        return f"Erro inesperado: {e}"

    #Bloco que sempre é executado para garantir que os recursos sejam liberados
    finally:
        if 'cursor' in locals():  # Verifica se a variável 'cursor' foi criada no escopo local da função (valida se a conexão foi aberta com sucesso)
            cursor.close()  # Fecha o cursor para liberar o recurso no banco de dados
        if 'conn' in locals() and conn.is_connected(): # Verifica se a variável 'conn' foi criada e se a conexão ainda está ativa
            conn.close()  # Fecha a conexão com o banco de dados

def gerar_id_unico(config): #Arg: config (dict): Configuração de conexão com o banco de dados.
    #1- Gera um ID único de paciente que não existe ainda na tabela 'pacientes'.
    #2- Verifica no banco se o ID gerado já está em uso.


    while True:
        novo_id = uuid.uuid4().hex[:8]  # Gera ID com 8 caracteres

        try:
            #Estabelecimento de conexão com o banco de dados usando as configurações passadas (estarão no main.py as configs)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            #Cursor vai procurar no banco de dados o ID gerado na coluna 'id' e tabela pacientes
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE id = %s", (novo_id,))
            (existe,) = cursor.fetchone() #Recupera o resultado da consulta (um único valor) e armazena na variável 'existe'

            if not existe: #Se não existe (ID é único)
                return novo_id  #Retorna esse novo ID

        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao verificar ID no banco: {err}")
            return None

        finally:
            if 'cursor' in locals():  #Verifica se a variável 'cursor' foi criada no escopo local da função (valida se a conexão foi aberta com sucesso)
                cursor.close()   #Fecha o cursor para liberar o recurso no banco de dados
            if 'conn' in locals() and conn.is_connected():  #Verifica se a variável 'conn' foi criada e se a conexão ainda está ativa
                conn.close() #Fecha a conexão com o banco de dados
import mysql.connector
import uuid

def registrar_receita_pdf(paciente_id, caminho_pdf, config):

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        with open(caminho_pdf, "rb") as file:
            pdf_data = file.read()

        cursor.execute("""
            INSERT INTO receitas (paciente_id, arquivo_pdf)
            VALUES (%s, %s)
        """, (paciente_id, pdf_data))

        conn.commit()
        return f"Receita para o paciente com ID {paciente_id} registrada com sucesso!"

    except mysql.connector.Error as err:
        return f"Erro de banco de dados: {err}"

    except Exception as e:
        return f"Erro inesperado: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def gerar_id_unico(config): # Arg: config (dict): Configuração de conexão com o banco de dados.
    # 1- Gera um ID único de paciente que não existe ainda na tabela 'pacientes'.
    # 2- Verifica no banco se o ID gerado já está em uso.


    while True:
        novo_id = uuid.uuid4().hex[:8]  # Gera ID com 8 caracteres

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE id = %s", (novo_id,))
            (existe,) = cursor.fetchone()

            if not existe:
                return novo_id  # Retorna se o ID ainda não existe

        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao verificar ID no banco: {err}")
            return None

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()
#Importa bibliotecas necessárias

from datetime import datetime  #Trabalha com datas e horários
import speech_recognition as sr  #Reconhecimento de voz
import smtplib  #Envia e-mails usando protocolo SMTP
from email.message import EmailMessage  #Cria e gerencia mensagens de e-mail
from fpdf import FPDF  # Biblioteca para gerar arquivos PDF
from database import *

# Configurações de conexão banco de dados - SP4
config = {
    'host': 'localhost', #Local do host
    'user': 'root', #usuario do mysql
    'password': 'joao', #senha do mysql
    'database': 'hospital_sabara' #nome do banco de dados no mysql
}

#Coleta dados do paciente -
def coletar_dados_pacientes(config):
    #Solicita ao usuário o nome do paciente
    nome = input("Digite o nome do paciente: ")
    #Solicita ao usuário o e-mail do paciente
    email = input("Digite o e-mail do paciente: ")
    #Gera um ID para o paciente automaticamente - SP4
    paciente_id = gerar_id_unico(config)
    cadastrar_paciente(paciente_id, nome, email, config) #Hipotético, pois o hospital ja possui um bd de pacientes
    #Exibe informações coletadas
    print(f"\n[INFO] Nome: {nome}")
    print(f"[INFO] E-mail: {email}")
    print(f"[INFO] ID gerado: {paciente_id}")


    #Retorna o nome e e-mail para uso posterior
    return nome, email, paciente_id

#Escuta a voz do médico
def ouvir_medico():
    #Armazena dentro da variável o reconhecedor de voz usando a biblioteca speech_recognition
    reconhecedor = sr.Recognizer()
    #Configura o microfone como fonte de áudio
    microfone = sr.Microphone()


    #Usa o microfone para capturar o áudio
    with microfone as entrada_audio: #Usado para abrir, usar e depois fechar automaticamente
        print("\n[INFO] Ajustando ruído de fundo... Aguarde um pouco.")
        #Faz o reconhecimento se adaptar ao ruído ambiente (barulhos de fundo), ajudando a melhorar a qualidade da transcrição
        reconhecedor.adjust_for_ambient_noise(entrada_audio)
        print("[INFO] Pode falar a prescrição agora:")
        #A variavel armazena, puxamos a variavel reconhecedor, capitura o áudio do microfone DURANTE 45 SEGUNDOS
        audio = reconhecedor.listen(entrada_audio, phrase_time_limit=45)


    try:
        #Usa o serviço da Google (gratuito) para transformar o áudio em texto. Aqui ele está configurado para o idioma português do Brasil
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        #Exibe o texto reconhecido
        print(f"\n[TRANSCRIÇÃO] Você disse: {texto}")
        return texto
    except sr.UnknownValueError:  #tratamentos de erros, ocorre quando o google não consegue entender o que foi falado
        #Caso não entenda o áudio
        print("[ERRO] Não entendi o que você falou.")
        return ""
    except sr.RequestError as erro: #tratamento de erros, ocorre quando não foi possível acessar o serviço do google
        #Caso tenha problema com o serviço de reconhecimento
        print(f"[ERRO] Problema com o serviço de reconhecimento: {erro}")
        return ""

#Preenche a receita no modelo
def preencher_receita_pdf(nome_paciente, receita_formatada):
    pdf = FPDF()  # Cria um documento PDF em branco e armazena na variavel pdf
    pdf.add_page()  # Adiciona uma nova página em branco no PDF
    pdf.set_font("Arial", size=12)  # Define a fonte inicial como Arial, tamanho 12


    # Obtém a data atual no formato brasileiro (ex: 15/04/2025)
    data_hoje = datetime.now().strftime("%d/%m/%Y")


    #Cabeçalho da Receita
    pdf.image("logo_sabara.png", x=60, y=10, w=90)  # Adiciona uma imagem centralizada no topo
    pdf.ln(30)  # Adiciona um espaço depois da imagem


    #Informações do paciente
    pdf.set_font("Arial", size=12)  # Volta a fonte normal, tamanho 12
    pdf.cell(200, 10, txt=f"Paciente: {nome_paciente}", ln=True)  # Escreve o nome do paciente
    pdf.cell(200, 10, txt=f"Data: {data_hoje}", ln=True)  # Escreve a data da receita
    pdf.ln(10)  # Linha em branco


    #Prescrição médica
    pdf.multi_cell(0, 10, txt=f"Prescrição:\n{receita_formatada}")  # Escreve a prescrição recebida do médico
    pdf.ln(20)  # Espaço antes da assinatura


    #Assinatura digital e rodapé com imagem
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Assinado digitalmente em: {data_hoje}", ln=True)
    pdf.ln(5)  # Espaço antes da imagem


    #Adiciona a imagem da assinatura
    pdf.image("assinatura_fake.png", x=60, w=90)  # x define a posição horizontal; w é a largura da imagem


    pdf.ln(20)  # Dá espaço depois da imagem, se precisar



    #Geração e salvamento do PDF
    nome_arquivo = f"receita_{uuid.uuid4().hex[:8]}.pdf"  # Cria um nome de arquivo com ID único
    caminho_saida = os.path.join(os.getcwd(), nome_arquivo)  # Define o caminho para salvar o arquivo na pasta atual


    pdf.output(caminho_saida)  # Salva o arquivo PDF no caminho definido


    # Mensagem final confirmando onde o PDF foi salvo
    print(f"\n✅ Receita PDF salva como: {caminho_saida}")


    return caminho_saida  # Retorna o caminho do arquivo gerado para uso posterior (ex: envio por e-mail)

#Envia e-mail com a receita
def enviar_email(destinatario, caminho_anexo, nome_paciente):
    # Cria um variável de e-mail que guarda: Assunto, Remetente, Destinatário, Corpo da mensagem, Anexo
    msg = EmailMessage()


    # Define o assunto do e-mail que o paciente vai ver na caixa de entrada
    msg["Subject"] = "Receita mágica digital"


    # Define o remetente (quem está enviando o e-mail)
    msg["From"] = "email_remetente"


    # Define o destinatário (o paciente que vai receber a receita)
    msg["To"] = destinatario


    # Define o corpo do e-mail com uma mensagem personalizada
    msg.set_content(f"""Olá, {nome_paciente}


Segue em anexo sua receita mágica.


Atenciosamente,
Hospital Sabará""")


    # Abre o arquivo do PDF gerado com a receita
    with open(caminho_anexo, "rb") as file: #Abre o arquivo PDF no modo leitura binária (rb) para poder anexar no e-mail
        conteudo = file.read()  # Lê o conteúdo binário do PDF
        nome_arquivo = os.path.basename(caminho_anexo)  # Pega só o nome do arquivo (sem o caminho) // "receita_a1b2c3d4.pdf"


        # Adiciona o PDF como anexo na mensagem
        msg.add_attachment(
            conteudo,  # conteúdo binário do arquivo
            maintype = "application",  # tipo principal do arquivo (arquivo genérico)
            subtype = "pdf",  # tipo específico (arquivo PDF)
            filename = nome_arquivo  # nome do arquivo que aparecerá no anexo
        )


    # Cria uma conexão segura com o servidor do Gmail pela porta 465
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # Faz login na conta do Gmail usando uma senha de aplicativo
        smtp.login("e-mail_medico", "senha_app_medico")


        # Envia a mensagem com o anexo para o destinatário
        smtp.send_message(msg)


    # Mensagem de confirmação no terminal
    print("✅ E-mail enviado com sucesso!")



#Execução principal
nome_paciente, email_paciente, paciente_id = coletar_dados_pacientes(config)

#Escuta a prescrição médica através do microfone
transcricao = ouvir_medico()


#Se conseguiu transcrever a prescrição
if transcricao != "":
    print(f"\n[TRANSCRIÇÃO] Receita reconhecida:\n{transcricao}")
    editar = input("Deseja editar a receita antes de gerar o PDF? (s/n): ")

    if editar == 's':
        tipo = input("Digite '1' para substituir por nova fala ou '2' para acrescentar algo: ")

        if tipo == '1':
            print("[INFO] Repita a nova prescrição:")
            nova_transcricao = ouvir_medico()

            if nova_transcricao != "":
                transcricao = nova_transcricao
            else:
                print("[ERRO] Nada foi reconhecido. Usando receita original.")

        elif tipo == '2':
            complemento = input("Digite o que deseja acrescentar: ")
            transcricao += f" {complemento}"

        else:
            print("Entrada inválida. A receita original será usada.")

    elif editar != 'n':
        print("A receita original será usada.")

    # Caminho do modelo de receita que será usado
    caminho_modelo = "receita_medica.docx"

    # Preenche a receita com os dados coletados
    caminho_receita = preencher_receita_pdf(nome_paciente, transcricao)

    # Salva o PDF no banco de dados
    mensagem_db = registrar_receita_pdf(paciente_id, caminho_receita, config)

    # Envia o e-mail com a receita em anexo
    enviar_email(email_paciente, caminho_receita, nome_paciente)

else:
    #Caso não tenha conseguido captar a prescrição, exibe mensagem de erro
    print("Nenhuma prescrição foi detectada, receita não gerada.")

visualizar_receita(paciente_id, config)

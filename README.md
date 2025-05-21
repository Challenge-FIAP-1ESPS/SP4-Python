# SP4-Python

# Receita Digital Automatizada – Hospital Sabará

Este projeto Python automatiza a criação e envio de receitas médicas digitais a partir da transcrição da voz do médico, integrando funcionalidades como:
- Reconhecimento de voz com transcrição
- Geração de receita em PDF
- Armazenamento em banco de dados MySQL
- Envio automático por e-mail com anexo

## Tecnologias utilizadas
- Python 3.x
- [speech_recognition](https://pypi.org/project/SpeechRecognition/)
- [fpdf](https://pyfpdf.github.io/fpdf2/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- smtplib / email
- MySQL 8.0+

## Estrutura do Projeto

```
projeto/
├── main.py                # Script principal que executa todo o fluxo
├── database.py            # Módulo com funções para banco de dados
├── logo_sabara.png        # Logotipo inserido na receita
├── assinatura_fake.png    # Imagem da assinatura digital
```

## Como executar

1. **Instale as dependências:**
```bash
pip install SpeechRecognition fpdf mysql-connector-python
```

2. **Configure o banco de dados MySQL:**

Crie o banco de dados e a tabela:

```sql
CREATE DATABASE hospital_sabara;

USE hospital_sabara;

CREATE TABLE pacientes (
    id VARCHAR(8) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE receitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id VARCHAR(8),
    arquivo_pdf LONGBLOB,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);
```

3. **Atualize as configurações de acesso ao banco em `main.py`:**
```python
config = {
    'host': 'localhost',
    'user': 'SEU_USUARIO',
    'password': 'SUA_SENHA',
    'database': 'hospital_sabara'
}
```

4. **Execute o projeto:**
```bash
python main.py
```

## Funcionalidades
- Captura da voz do médico
- Geração automática de receita em PDF com logotipo e assinatura
- Armazenamento do PDF no banco de dados (MySQL)
- Envio da receita por e-mail para o paciente

## Observações
- O envio de e-mail requer autenticação com **senha de app** (como no Gmail).
- O microfone deve estar funcionando corretamente para a captura de voz.

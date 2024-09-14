import os
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para conectar ao Google Sheets
def connect_google_sheets(sheet_id, worksheet_name):
    # Escopos de permissões necessárias
    scope = ['https://www.googleapis.com/auth/spreadsheets', 
             'https://www.googleapis.com/auth/drive.file']
    
    credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    
    # Autenticação usando o arquivo de credenciais
    creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
    client = gspread.authorize(creds)
    
    try:
        # Abre a planilha pelo ID
        spreadsheet = client.open_by_key(sheet_id)
    except gspread.SpreadsheetNotFound as e:
        print(f"Planilha não encontrada: {e}")
        raise

    try:
        # Abre a aba (worksheet) pelo nome
        sheet = spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound as e:
        print(f"Aba não encontrada: {e}")
        raise

    return sheet


# Função para enviar e-mails
def send_email(subject, body, recipient_email, sender_email, sender_password):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"E-mail enviado com sucesso para {recipient_email}")
    except Exception as e:
        print(f"Falha ao enviar e-mail para {recipient_email}: {str(e)}")

# Função principal para ler o Google Sheets e enviar os e-mails
def send_bulk_emails_google(sheet_name, worksheet_name, subject, body_template):
    sheet = connect_google_sheets(sheet_name, worksheet_name)
    recipients = sheet.get_all_records()

    # Pega os detalhes do remetente do .env
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    for recipient in recipients:
        name = recipient['nome']
        email = recipient['email']
        # Personalize o corpo do e-mail se necessário
        body = body_template.replace('{nome}', name)
        send_email(subject, body, email, sender_email, sender_password)

# Exemplo de uso
sheet_name = 'id planilha' # Id da planilha do Google Sheets 
worksheet_name = 'emails'  # Nome da aba/worksheet na planilha
subject = 'Sua Oferta Especial'
body_template = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
        }
        h1 {
            color: #333333;
        }
        p {
            font-size: 16px;
            color: #666666;
        }
        .button {
            display: inline-block;
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            margin-top: 20px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Olá {nome},</h1>
        <p>Gostaríamos de compartilhar uma oferta exclusiva com você. Aproveite essa oportunidade especial e confira nossas últimas novidades.</p>
        <p>Clique no botão abaixo para saber mais:</p>
        <a href="https://suaempresa.com" class="button">Ver Oferta</a>
        <p>Atenciosamente,<br>Sua Empresa</p>
    </div>
</body>
</html>
'''

# Enviar os e-mails
send_bulk_emails_google(sheet_name, worksheet_name, subject, body_template)

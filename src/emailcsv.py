import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()
# Função para ler os dados do CSV
def read_csv(file_path):
    recipients = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipients.append(row)
    return recipients

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

# Função principal para ler o CSV e enviar os e-mails
def send_bulk_emails(csv_file, subject, body_template):
    recipients = read_csv(csv_file)

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
csv_file = '../email.csv' # path para o csv
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
send_bulk_emails(csv_file, subject, body_template)


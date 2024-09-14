### **Projeto: Automação de Envio de Emails em Massa**

#### **Objetivo do Projeto**
A automação foi criada para resolver o problema de envio em massa de emails para uma lista grande de destinatários, de maneira eficiente e com baixo risco de erros. O foco principal é evitar o envio manual, que pode ser demorado e propenso a falhas.

#### **Ferramentas e Tecnologias Utilizadas**
- **Linguagem**: Python 3
- **APIs**: Google Sheets API, Gmail API
- **Outras tecnologias**: Google Cloud Platform (GCP) para habilitar as APIs e integração com o Google Sheets
- **Bibliotecas Python**: `MIMEText`, `MIMEMultipart`, `smtplib`, `csv`, `gspread`, `google.oauth2.service_account`

#### **Estrutura do Projeto**
A automação lê dados de duas fontes principais:
1. **CSV local**: Um arquivo contendo os emails e nomes dos destinatários.
2. **Google Sheets**: Uma planilha online integrada via Google Sheets API.

Com base nos dados lidos de cada fonte, o script envia emails personalizados para cada destinatário.

#### **Funcionamento**
O processo de funcionamento é simples e eficiente:
1. A automação verifica se as bibliotecas necessárias estão instaladas (Python 3 e dependências via `pip`).
2. O script faz a leitura da lista de emails e nomes do destinatário, seja a partir de um arquivo CSV local ou diretamente de uma planilha do Google Sheets.
3. Com base nas informações obtidas, o script utiliza a API do Gmail para enviar emails em massa.
4. Cada email é enviado individualmente para evitar o bloqueio do provedor de email por envios em massa.

#### **Configurações Específicas**
Para utilizar a automação, é necessário:
- **Google App Password**: Um app password gerado na conta do Google para autorizar o envio de emails sem precisar inserir as credenciais diretamente no código.
- **Service Account JSON**: Um arquivo `service_account.json` gerado no Google Cloud Platform para autenticar o script e permitir o acesso à planilha do Google Sheets.
  
  Ambos os arquivos precisam ser configurados corretamente no ambiente onde a automação será executada.

#### **Resultados e Benefícios**
Com essa automação, o envio de emails para grandes listas de destinatários é acelerado, poupando horas de trabalho manual e reduzindo a chance de erros, como esquecimentos ou duplicação de envios. A automação pode ser usada para campanhas de marketing, notificações ou atualizações para grandes grupos de pessoas.

#### **Passos de Execução**
1. Certifique-se de que Python 3 e as bibliotecas necessárias estejam instaladas.
   - Instale as dependências com: `pip install -r requirements.txt`.
   
2. Para enviar emails a partir de um CSV:
   - Execute o comando: `python3 emailcsv.py`
   
3. Para enviar emails a partir do Google Sheets:
   - Execute o comando: `python3 emailGSheets.py`
   
   **Observação**: Esta automação foi testada em ambiente Linux, e pode ser necessário ajustar o caminho dos arquivos ou dependências para funcionar no Windows ou MacOS.

#### **Possíveis Melhorias Futuras**
- Integração com outras plataformas de email (Outlook, SendGrid, etc.).
- Implementação de uma fila de envio para evitar que grandes volumes de emails sejam enviados de uma vez e fiquem retidos em filtros de spam.
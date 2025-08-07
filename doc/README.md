# Middleware Azure DevOps ↔ Telegram

## 📌 Visão Geral

Este middleware é responsável por monitorar *work items* do Azure DevOps e notificar um grupo no Telegram automaticamente, sempre que houver novos registros de acordo com uma *query* configurada.

---

## 🧠 Como Funciona

1. O código Python consome periodicamente a API do Azure DevOps (via Query).
2. Ele verifica se há novos itens (não notificados anteriormente).
3. Se encontrar novos, envia uma mensagem com os detalhes para o grupo no Telegram.
4. Salva localmente os IDs já notificados, evitando duplicidade.

---

## 📱 Telegram

### ✅ Etapas para configurar o bot

1. **Criar o bot**  
   Acesse o [@BotFather](https://t.me/BotFather) no Telegram e envie o comando `/newbot`.  
   Siga as instruções e ao final você receberá o **TOKEN do bot**.

2. **Ativar o bot**  
   Envie uma mensagem qualquer para o seu novo bot no Telegram para ativá-lo.

3. **Criar grupo**  
   Crie um grupo no Telegram e adicione o bot criado como membro.

4. **Permissões do bot no grupo**  
   O bot precisa de permissão para:
   - Ler mensagens (em grupos públicos)
   - Enviar mensagens

5. **Obter o ID do grupo**  
   Utilize um bot como [@userinfobot](https://t.me/userinfobot) ou gere logs no próprio middleware para obter o `chat_id`.

---

## 💻 Azure DevOps

## 🧪 Query no Azure DevOps

### 1. Acesse o Azure DevOps
- Vá para `Boards` > `Queries`
- Crie uma query como:

Work Item Type = Bug  
State != Closed  
Assigned To = [Equipe X]


### 2. Salve a query e copie a URL de execução
A URL deve ser usada na variável de ambiente ou diretamente no código.

---

## 🐍 Código Python

### Estrutura do Projeto
```text
middleware-azure-telegram/
├── src/
│   ├── main.py
├── test/
│   └── test_envio_telegram.py
│   └── test_main.py
│   └── test_persistencia_ids.py
├── requirements.txt
├── README.md
└── .env
```

* * *

🧪 Exemplos de Payload
----------------------

### 🔄 Resposta da API de Work Items


`{   "id": 12345,   "fields": {     "System.Title": "Bug crítico na produção",     "System.State": "Ativo",     "System.CreatedDate": "2025-08-01T13:45:00Z",     "System.AssignedTo": {       "displayName": "Fulano da Silva"     }   } }`

### 📩 Mensagem enviada ao Telegram

```markdown
Novo Work Item Cadastrado:
ID: 131963  
Título: novo task teste telegram  
Estado: Done  
 [![🔗](https://web.telegram.org/a/img-apple-64/1f517.png) Abrir no Azure DevOps](https://dev.azure.com/SME-Spassu/SME%20-%20Treinamento/_workitems/edit/131963 "https://dev.azure.com/SME-Spassu/SME - Treinamento/_workitems/edit/131963")  
tipo:Desconhecido
```
* * *

⚙️ Variáveis Importantes
------------------------

| Variável | Descrição | Valor
| --- | --- | --- |
|AZURE_ORGANIZATION | Nome da organização no Azure devops |https://dev.azure.com/SME-Spassu
|AZURE_PROJECT| Nome do projeto a ser enviado | SME - Treinamento
|AZURE_PAT| a89a7dy8d89awy7dhya9wdy |TOKEN OBTIDO NO AZURE DEVOPS
|TELEGRAM_TOKEN | TOKEN DO BOT Fornecido pelo BOT FATHER |7843389099:AAFV6tudC8kf4W0691Z_m3Uynrj1ttupLcQ
|TELEGRAM_CHAT_ID | ID Do grupo que o BOT irá postar as mensagens |-1002667238649 
|POLL_INTERVAL|Tempo de refresh do buscador de itens python|10|

* * *

✅ Requisitos
------------

*   Python 3.10+
    
*   `requests`, `python-dotenv`, `pytest`, `unittest`, `coverage`
    

* * *


🔐 Segurança
------------

*   Nunca exponha seu `TELEGRAM_TOKEN` publicamente.
    
*   Considere usar `.env` e `python-dotenv` para configurar as variáveis de ambiente.
    
* Criar um usuário para telegram e azure devops e cadastrar seus ids no cofre de senhas 
* O Azure PAT é um PERSONAL ACCESS TOKEN, portanto deve ser de uso pessoal e intransferível
* * *

📌 Observações
--------------

*   O serviço não usa banco de dados. Os IDs são persistidos em `last_ids.json`.
    
*   Para ambientes de produção, considere:
    *   Monitoramento com logs centralizados
        
    *   Execução como serviço (ex: Docker, com Rancher)
        
    *   Tolerância a falhas e _backoff_ para a API do Azure
    
    *   Criação de base de dados para armazenar os id´s enviados

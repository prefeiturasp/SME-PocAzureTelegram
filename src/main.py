import requests
import time
import json
import base64
from dotenv import load_dotenv
import os


load_dotenv()

AZURE_ORG = os.getenv("AZURE_ORGANIZATION")
AZURE_PROJECT = os.getenv("AZURE_PROJECT")
AZURE_PAT = os.getenv("AZURE_PAT")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

QUERY_DAYS_AGO = int(os.getenv("QUERY_DAYS_AGO", 2))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 10))

STATE_FILE = 'last_ids.json'

# Gera header com autenticação
pat_token = f":{AZURE_PAT}"
b64_pat = base64.b64encode(pat_token.encode()).decode()
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {b64_pat}'
}

def carregar_ids():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def salvar_ids(ids):
    with open(STATE_FILE, 'w') as f:
        json.dump(ids, f)

def buscar_work_items():
    url = f"{AZURE_ORG}/{AZURE_PROJECT}/_apis/wit/wiql?api-version=7.0"
    query = {
        "query": """SELECT [System.Id]
                    FROM WorkItems
                    WHERE [System.TeamProject] = 'SME - Treinamento'
                    AND [System.ChangedDate] > @startOfDay('-2d')
                    ORDER BY [System.ChangedDate] DESC"""
    }
    r = requests.post(url, headers=headers, json=query)
    r.raise_for_status()
    result = r.json()
    return [item['id'] for item in result.get('workItems', [])]


def buscar_detalhes(item_id):
    url = f"{AZURE_ORG}/{AZURE_PROJECT}/_apis/wit/workitems/{item_id}?api-version=7.0"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def verificar():
    ids = buscar_work_items()
    conhecidos = carregar_ids()
    novos = [i for i in ids if i not in conhecidos]
    
    for item_id in novos:
        detalhe = buscar_detalhes(item_id)
        titulo = detalhe['fields'].get('System.Title', 'Sem título')
        estado = detalhe['fields'].get('System.State', 'Desconhecido')
        url = f"{AZURE_ORG}/{AZURE_PROJECT}/_workitems/edit/{item_id}"
        msg = f"*Novo Work Item Cadastrado:*\nID: {item_id}\nTítulo: {titulo}\nEstado: {estado}\n[🔗 Abrir no Azure DevOps]({url})"
        print(msg)        
        enviar_telegram(msg)

    salvar_ids(ids[:20])  # guarda os últimos 20

if __name__ == "__main__":
    while True:
        try:
            verificar()
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(POLL_INTERVAL)

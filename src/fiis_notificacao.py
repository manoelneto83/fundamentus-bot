from utils import *

# Passo 1: importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import date
import pandas as pd
import argparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import schedule

load_dotenv()

ATIVO_COLUMN = 'Papel'
SEGMENTO_COLUMN = 'Segmento'
COTACAO_COLUMN = 'Cotação'
DY_COLUMN = 'Dividend Yield'
PVP_COLUMN = 'P/VP'
LIQUIDEZ_COLUMN = 'Liquidez'
QTDE_IMOVEIS = 'Qtd de imóveis'
VACANCIA_COLUMN = 'Vacância Média'
PRECO_ALVO_COLUMN = 'preco_alvo'
DATA_ENVIADO_COLUMN = 'ENVIADO'
DB_NAME = 'database.db'


def execute():
    # Marca o tempo de início
    print(f"Executando... {datetime.today()}")
    inicioTempo = time.time()

    base_url = "https://www.fundamentus.com.br/fii_resultado.php"
    # Realizar a requisição HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(base_url, headers=headers)
    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Fazer o parsing do HTML usando BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar a tabela HTML (pode ser necessário inspecionar a página para obter o seletor correto)
        html_tabela = soup.find("table")

        # Ler a tabela HTML com pd.read_html
        # df = pd.read_html(str(html_tabela))[0]  # Supondo que haja apenas uma tabela na página

    else:
        print("Falha na requisição HTTP. Código de status:", response.status_code)
        raise

    tabela = pd.read_html(str(html_tabela))[0]
    tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN].str.replace(
        ',', '').str.replace('.', '').astype(float) / 100

    tabela_customizada = tabela[[ATIVO_COLUMN,
                                SEGMENTO_COLUMN,
                                COTACAO_COLUMN,
                                DY_COLUMN,
                                PVP_COLUMN,
                                LIQUIDEZ_COLUMN,
                                QTDE_IMOVEIS,
                                VACANCIA_COLUMN]]

    tabela_customizada.set_index(ATIVO_COLUMN)

    df_lista_preco_alvo = pd.read_csv('fiis_preco_alvo.csv')
    df_lista_preco_alvo[PRECO_ALVO_COLUMN] = df_lista_preco_alvo[PRECO_ALVO_COLUMN].str.replace(
        ',', '').str.replace('.', '').astype(float) / 100

    # print(df_lista_preco_alvo)

    # Remover repetições na coluna 'segmento'
    list_ativos = df_lista_preco_alvo[ATIVO_COLUMN].unique()
    # Remove os itens vazios da lista
    list_ativos = list(filter(None, list_ativos))

    df_ativos_encontrados = tabela_customizada[tabela_customizada[ATIVO_COLUMN].isin(
        list_ativos)]

    df_ativos_encontrados.set_index(ATIVO_COLUMN)
    print("ativos encontrados:")
    print(df_ativos_encontrados)

    df_database = pd.DataFrame()
    try:
        # Tentar ler o arquivo CSV
        df_database = pd.read_csv(DB_NAME)
        df_database.set_index(ATIVO_COLUMN)
        # Se o arquivo não existir, df será um DataFrame vazio
        print(df_database)
    except FileNotFoundError:
        print("O arquivo database.db não existe.")

    # df_database.set_index(ATIVO_COLUMN)

    # Realiza o join usando a coluna 'Papel'
    df_merged = pd.merge(df_ativos_encontrados,
                         df_lista_preco_alvo, on=ATIVO_COLUMN)
    print("merged1:")
    print(df_merged)

    if not df_database.empty:
        df_merged = pd.merge(df_merged,
                             df_database, on=ATIVO_COLUMN, how='outer')
        df_merged[DATA_ENVIADO_COLUMN].fillna(0, inplace=True)

    print("merged2:")
    print(df_merged)

    df_resultado = df_merged[(df_merged[COTACAO_COLUMN]
                              <= df_merged[PRECO_ALVO_COLUMN])]
    print('resultado filtro cotacao:')
    print(df_resultado)

    if DATA_ENVIADO_COLUMN in df_resultado.columns:
        df_resultado = df_resultado[(
            df_resultado[DATA_ENVIADO_COLUMN] == 0)]

        print("filtrando por ENVIADO")

    print('resultado filtro enviado:')
    print(df_resultado)
    print(f"encontratos: {df_resultado.shape[0]}")
    content_list = []
    for index, row in df_resultado.iterrows():
        content = f"O {row[ATIVO_COLUMN]} atingiu o preço alvo de {row['preco_alvo']}. Sua cotação é: {row[COTACAO_COLUMN]}"
        content_list.append(content + "\n")
        df_resultado.at[index, DATA_ENVIADO_COLUMN] = date.today()
    print(f"content fora {content_list}")
    # enviar email
    if not df_resultado.empty:
        df_resultado = df_resultado[[ATIVO_COLUMN, DATA_ENVIADO_COLUMN]]
        df_enviados = pd.concat([df_resultado, df_database], ignore_index=True)

        df_enviados.to_csv(DB_NAME)
        print('Salvando os dados')
        print(df_enviados)
        print('enviar email')
        content_result = ''.join(content_list)
        print("content result:")
        print(content_result)
        sendEmail(content_result)
    else:
        print(f"Email já enviado na data de hoje: {date.today()}")
    # Marca o tempo de término
    fimTempo = time.time()

    # Calcula o tempo decorrido
    tempo_decorrido = fimTempo - inicioTempo
    print(f"Tempo decorrido: {format2decimal(tempo_decorrido)} segundos")

    # print(resultado)
    # print(f"rows: {resultado.shape[0]}")


def format2decimal(valor):
    return float("{:.2f}".format(valor))


data_expiracao = datetime(2024, 12, 31)


def sendEmail(content):
    senha = os.environ.get('SENHA_EMAIL')
    email_remetente = 'manoelneto83@gmail.com'
    email_destinatario = os.environ.get('EMAIL_DESTINATARIO')

    msg = EmailMessage()
    msg['Subject'] = "Notificação de ativos com preço alvo - [Método2Em1]"
    msg['From'] = email_remetente
    msg['To'] = email_destinatario

    msg.set_content(f''' Prezado Membro do Método2Em1, segue notificação dos ativos que atigiram o seu preço alvo:

    <p>{content.strip()}</p>



    Abs,

    Método2Em1 o melhor curso do Brasil

    ''')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        print('enviando email...')
        smtp.login(email_remetente, senha)
        smtp.send_message(msg)

#########################################################################


if datetime.now() > data_expiracao:
    print("Por favor, obtenha uma versão mais recente.")
    exit()

# Agende a função para ser executada a cada 10 minutos
minutos = 5
print(f"Monitoramento iniciado, verificação a cada {minutos} minutos...")
schedule.every(minutos).minutes.do(execute)

while True:
    # Execute as tarefas agendadas
    schedule.run_pending()
    time.sleep(1)  # Aguarde um segundo antes de verificar novamente

execute()

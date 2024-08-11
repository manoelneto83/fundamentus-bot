# Esse bot está definido para se integrar com o rocket web chat

import pyautogui
import pyperclip
import time
# from datetime import datetime
from datetime import datetime, date
import math
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.common.exceptions import NoSuchElementException
from utils import *
from os import environ, path, curdir
from dotenv import load_dotenv
import pandas as pd


# Find .env file
basedir = path.abspath(curdir)
load_dotenv(path.join(basedir, '.env'))

# configura o tempo de forma global
pyautogui.PAUSE = 0.5
login_user_redmine = environ.get('LOGIN_USER_REDMINE')
login_password_redmine = environ.get('LOGIN_PASSWORD_REDMINE')
login_user_rocket = environ.get('LOGIN_USER_ROCKET')
login_password_rocket = environ.get('LOGIN_PASSWORD_ROCKET')

path_img = "./src/img/"
path_web_driver = environ.get('PATH_WEB_DRIVER')
horasAlvo = 6

ATIVO_COLUMN = 'ativo'
VALOR_PAGTO_COLUMN = 'valor_pagto'
DATA_PAGTO_COLUMN = 'data_pagto'

DB_NAME = 'database.db'
FILE_LISTA_ATIVOS = 'lista_ativos.csv'
# Caminho para o arquivo CSV


# Carregar o arquivo CSV para um DataFrame
df_ativos = pd.read_csv(FILE_LISTA_ATIVOS)

# Extrair a lista de ativos da coluna "ativos" do DataFrame
ativos_carteira = df_ativos["ativos"].tolist()
tipo_ativos_carteira = df_ativos["tipo"].tolist()


# Exibir a lista de ativos
print(ativos_carteira)


links = "https://statusinvest.com.br/fundos-imobiliarios/{}"
link_acao = "https://statusinvest.com.br/acoes/{}"


def execute():
    obter_dados()
    notificar()


def notificar():
    for i in range(len(ativos_carteira)):
        try:
            imprimir(
                f"Iniciando o fluxo de notificacao para o ativo: {ativos_carteira[i]}")

            df_database = pd.DataFrame(
                columns=[ATIVO_COLUMN, VALOR_PAGTO_COLUMN, DATA_PAGTO_COLUMN])
            try:
                # Tentar ler o arquivo CSV
                df_database = pd.read_csv(DB_NAME)
                df_database.set_index(ATIVO_COLUMN)
                # Se o arquivo não existir, df será um DataFrame vazio
                print(df_database)
            except FileNotFoundError:
                raise FileNotFoundError("O arquivo database.db nao existe.")

            is_ativo_exist = ativos_carteira[i] in df_database['ativo'].values

            print("is_ativo_exist:", is_ativo_exist)

            if not is_ativo_exist:
                print(
                    f"ativo nao encontrado para ser notificado, nao existe dados para esse ativo: {ativos_carteira[i]}")
                continue

            row_corrente = df_database[df_database[ATIVO_COLUMN]
                                       == ativos_carteira[i]]

            if row_corrente.empty:
                continue

            data_pagamento = pd.to_datetime(
                row_corrente[DATA_PAGTO_COLUMN].iloc[0], format='%d/%m/%Y').date()

            data_hoje = datetime.datetime.today().date()

            print(f'row_corrente {row_corrente}')
            print(row_corrente[VALOR_PAGTO_COLUMN].iloc[0])
            print(f'data_pagamento {data_pagamento}')
            print(f'data_hoje {data_hoje}')

            # 3. Verificar se a data de pagamento é hoje
            if data_pagamento == data_hoje:
                print("Hoje é a data do pagamento.")
                sendEmail(
                    f'O ativo {ativos_carteira[i]} pagou {row_corrente[VALOR_PAGTO_COLUMN].iloc[0]} por cota')

            # 4. Excluir registros com data de pagamento anterior à data de hoje
            elif data_pagamento < datetime.datetime.today().date():
                df_database = df_database[df_database[ATIVO_COLUMN]
                                          != ativos_carteira[i]]
                df_database.to_csv(DB_NAME, index=False)
                print(
                    'Excluindo Ativos que a data de pagamento ja passou...', ativos_carteira[i])

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            raise


def obter_dados():
    for i in range(len(ativos_carteira)):
        try:
            imprimir(f"Iniciando o fluxo para o ativo: {ativos_carteira[i]}")

            df_database = pd.DataFrame(
                columns=[ATIVO_COLUMN, VALOR_PAGTO_COLUMN, DATA_PAGTO_COLUMN])
            try:
                # Tentar ler o arquivo CSV
                df_database = pd.read_csv(DB_NAME)
                df_database.set_index(ATIVO_COLUMN)
                # Se o arquivo não existir, df será um DataFrame vazio
                print(df_database)
            except FileNotFoundError:
                print("O arquivo database.db nao existe.")

            if not df_database.empty:
                print("O DataFrame NAO esta vazio.")
                # df_database = df_database[ATIVO_COLUMN].unique()
                # # Remove os itens vazios da lista
                # df_database = list(filter(None, df_database))

                is_ativo_exist = ativos_carteira[i] in df_database['ativo'].values

                print("is_ativo_exist:", is_ativo_exist)

                if is_ativo_exist:
                    print("ativo ja existe no banco de dados")
                    continue

                df_dados = obter_dados_pagamento(
                    ativos_carteira[i],
                    df_database,
                    tipo_ativos_carteira[i])

                df_dados.to_csv(DB_NAME, index=False)
                print('Salvando os dados em arquivo...')
            else:
                df_dados = obter_dados_pagamento(
                    ativos_carteira[i],
                    df_database,
                    tipo_ativos_carteira[i])

                df_dados.to_csv(DB_NAME, index=False)
                print('Salvando os dados em arquivo...')

        except ValueError as err:
            imprimir(f"Ocorreu um erro: {err}")

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            raise


def obter_dados_pagamento(ativo_corrente, df_database, tipo_ativo_corrente):
    imprimir("Abrindo o navegador chrome...")
    navegador = openChrome()

    if tipo_ativo_corrente == 'FII':
        linkAtual = links.format(ativo_corrente)
    else:
        linkAtual = link_acao.format(ativo_corrente)

    pyperclip.copy(linkAtual)
    url = pyperclip.paste()
    navegador.get(url)
    time.sleep(5)
    navegador.execute_script(f"window.scrollTo(0, {1500})")
    time.sleep(5)

    if tipo_ativo_corrente == 'FII':
        valor_pagto = navegador.find_element(
            'xpath', '//*[@id="main-2"]/div[2]/div[7]/div[3]/div/div[1]/strong').text
    else:  # acao
        valor_pagto = navegador.find_element(
            'xpath', '//*[@id="earning-section"]/div[7]/div/div[2]/table/tbody/tr[1]/td[4]').text

    valor_pagto = valor_pagto.replace(",", ".")

    if not is_float(valor_pagto):
        print("Dados ainda nao informados pelo site")
        raise ValueError("Dados ainda nao informados pelo site")

    valor_pagto = float(valor_pagto)
    print(f"valor_pagto-> {valor_pagto:.2f}")

    if tipo_ativo_corrente == 'FII':
        data_pagto = navegador.find_element(
            'xpath', '//*[@id="main-2"]/div[2]/div[7]/div[3]/div/div[2]/div[2]/div[2]/div/b').text
    else:
        data_pagto = navegador.find_element(
            'xpath', '//*[@id="earning-section"]/div[7]/div/div[2]/table/tbody/tr[1]/td[3]').text

    print(f"data_pagto-> {data_pagto}")

    imprimir("fechando navegador...")
    navegador.quit()

    novo_registro = {ATIVO_COLUMN: ativo_corrente,
                     'valor_pagto': valor_pagto,
                     'data_pagto': data_pagto}

    # Adicionar o novo registro ao DataFrame
    # df_database = df_database.append(novo_registro, ignore_index=True)
    df_database.loc[len(df_database)] = novo_registro
    print('dados coletados', df_database)

    return df_database


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


execute()

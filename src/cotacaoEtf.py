# Esse bot está definido para se integrar com o rocket web chat

import pyautogui
import pyperclip
import time
import datetime
import logging
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
# configurando os logs
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    filename=f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}-cotacaoEtf.log",
                    filemode="w")


ativos = [
    "BOVA11",
    "IVVB11",
]

celulas = [
    "D8",
    "D9",
]

links = [
    "https://investidor10.com.br/etfs/{}/",
    "https://investidor10.com.br/etfs/{}/",

]


def execute():
    for i in range(len(ativos)):
        try:
            imprimir(f"Iniciando o fluxo para o ativo: {ativos[i]}")
            time.sleep(5)
            imprimir("Abrindo o navegador chrome...")
            # openAndMaximizedApp("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", 0)
            navegador = openChrome()

            linkAtual = links[i].format(ativos[i])
            pyperclip.copy(linkAtual)
            url = pyperclip.paste()
            navegador.get(url)

            cotacao_atual = navegador.find_element(
                'xpath', '//*[@id="cards-ticker"]/div[1]/div[2]/div/span').text
            cotacao_atual = cotacao_atual.replace("R$ ", "")

            imprimir(f"cotacao atual {cotacao_atual}")

            openAndMaximizedApp(
                "https://docs.google.com/spreadsheets/d/1ND_kM4sd0P3joJg4OSjFw4-6pYz4xL04aEpmZAkIn04/edit#gid=271190194", 5)

            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            time.sleep(5)
            click(f"{path_img}input_celula.png", 25)
            time.sleep(1)

            imprimir(f"selecionando celula {celulas[i]}")
            pyautogui.write(celulas[i])
            pyautogui.press("enter")
            imprimir(f"escrevendo cotação atual")
            pyautogui.write(cotacao_atual)
            pyautogui.press("enter")
            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            imprimir("fechando navegador...")
            navegador.quit()

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            raise

            # escrevendo o dy12Meses
            time.sleep(2)
            click(f"{path_img}input_celula.png", 25)
            time.sleep(1)

    imprimir("fim ETFs")


execute()

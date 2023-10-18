# Esse bot está definido para se integrar com o rocket web chat

import pyautogui
import pyperclip
import time
import datetime
import logging
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
                    filename=f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}-xerife.logs",
                    filemode="w")


ativos = [
    "POSI3",
    "USIM5",
    "BBAS3",
    "TAEE11",
    "SAPR11",
    "TRPL4",
    "VIVT3",
    "VALE3",
    "PETR4",
    "TECN3",
    "KLBN4",
    "RANI3",
    "BMGB4",
    "MRFG3",
    "CMIG4",
    "CBAV3",
    "CMIN3",
    "ITSA4",
    "CPLE3",
    "ITUB4",
    "GOAU4",
    "KEPL3",
    "SANB11",
    "BBSE3",
    "AESB3",
    "UNIP6",
    "BRKM5",
]

celulas = [
    "H18",
    "H19",
    "H20",
    "H21",
    "H22",
    "H23",
    "H24",
    "H25",
    "H26",
    "H37",
    "H38",
    "H39",
    "H40",
    "H41",
    "H42",
    "H43",
    "H44",
    "H45",
    "H46",
    "H30",
    "H31",
    "H32",
    "H47",
    "H48",
    "H49",
    "H50",
    "H51",


]

celulas_graham = [
    "J18",
    "J19",
    "J20",
    "J21",
    "J22",
    "J23",
    "J24",
    "J25",
    "J26",
    "J37",
    "J38",
    "J39",
    "J40",
    "J41",
    "J42",
    "J43",
    "J44",
    "J45",
    "J46",
    "J30",
    "J31",
    "J32",
    "J47",
    "J48",
    "J49",
    "J50",
    "J51",


]


scrolls = [
    2500,
    2500,
    2780,
    2780,
    2500,
    2500,
    2500,
    2500,
    2780,
    2500,
    2500,
    2500,
    2500,
    2500,
    2500,
    2500,
    2500,
    2780,
    2780,
    2500,
    2500,
    2500,
    2500,
    2500,
    2780,
    2500,
    2500,
]
links = [
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",
    "https://statusinvest.com.br/acoes/{}",

]


def execute():
    for i in range(len(ativos)):
        try:
            imprimir(f"Iniciando o fluxo para o ativo: {ativos[i]}")
            # time.sleep(5)
            imprimir("Abrindo o navegador chrome...")
            # openAndMaximizedApp("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", 0)
            navegador = openChrome()

            linkAtual = links[i].format(ativos[i])
            pyperclip.copy(linkAtual)
            url = pyperclip.paste()
            navegador.get(url)
            time.sleep(5)
            navegador.execute_script(f"window.scrollTo(0, {1800})")
            time.sleep(5)

            preco_justo = str(preco_justo_graham(navegador))
            print(f"preco_justo-> {preco_justo}")

            # preco_teto = preco_teto_bazim(navegador, scrolls[i])

            openAndMaximizedApp(
                "https://docs.google.com/spreadsheets/d/1ND_kM4sd0P3joJg4OSjFw4-6pYz4xL04aEpmZAkIn04/edit#gid=271190194", 5)

            # so pra tirar o mouse de cima da imagem
            pyautogui.moveTo(100, 100)

            time.sleep(3)
            click(f"{path_img}input_celula.png", 25)
            time.sleep(1)

            imprimir(f"selecionando celula graham {celulas_graham[i]}")
            pyautogui.write(celulas_graham[i])
            pyautogui.press("enter")
            imprimir(f"escrevendo preço justo de graham")

            pyautogui.write(preco_justo.replace(".", ","))
            pyautogui.press("enter")

            # time.sleep(3)
            # click(f"{path_img}input_celula.png", 25)
            # time.sleep(1)

            # imprimir(f"selecionando celula {celulas[i]}")
            # pyautogui.write(celulas[i])
            # pyautogui.press("enter")
            # imprimir(f"escrevendo preço teto")
            # pyautogui.write(preco_teto)
            # pyautogui.press("enter")

            imprimir("fechando navegador...")
            navegador.quit()

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            raise

    imprimir("fim PrecoTeto")


def preco_justo_graham(navegador):
    print(f"antes passei aqui manoel {navegador}")
    vpa = navegador.find_element(
        'xpath', '/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[9]/div/div/strong').text
    print(f"passei aqui manoel")
    vpa = vpa.replace(",", ".")

    vpa = float(vpa)
    print(f"vpa-> {vpa}")

    lpa = navegador.find_element(
        'xpath', '/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[11]/div/div/strong').text

    lpa = lpa.replace(",", ".")
    lpa = float(lpa)

    print(f"vpa-> {lpa}")

    num = 22.5 * lpa * vpa
    print(f"22.5 * lpa * vpa-> {num}")

    num_negativo = False
    if (num < 0):
        num = num * -1
        num_negativo = True

    raiz = math.sqrt(num)
    if (num_negativo):
        raiz = raiz * -1

    print(f"raiz-> {raiz}")

    return raiz


def preco_teto_bazim(navegador, scroll_atual):

    botao_5anos = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[1]/div[2]/ul/li[2]/a')

    navegador.execute_script(f"window.scrollTo(0, {scroll_atual})")
    time.sleep(5)
    navegador.execute_script("arguments[0].click();", botao_5anos)

    botao_agruparPorAno = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[5]/label/span[2]')

    time.sleep(5)
    navegador.execute_script(
        "arguments[0].click();", botao_agruparPorAno)

    time.sleep(1)
    print(pyautogui.position())
    print(botao_agruparPorAno.location)
    print(botao_agruparPorAno.location['y'] - scroll_atual)
    # movendo o mouse para o grafico ano atual -1 e obtendo o devidendo desse ano
    pyautogui.moveTo(896,
                     390,
                     0.5,
                     pyautogui.easeOutQuad)
    time.sleep(1)
    dividendo_ano_menos_1 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_1)

    # movendo o mouse para o grafico ano atual -2 e obtendo o devidendo desse ano
    pyautogui.moveTo(712, 390, 0.5, pyautogui.easeOutQuad)
    time.sleep(1)
    dividendo_ano_menos_2 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_2)

    # movendo o mouse para o grafico ano atual -3 e obtendo o devidendo desse ano
    pyautogui.moveTo(500, 390, 0.5, pyautogui.easeOutQuad)
    time.sleep(1)
    dividendo_ano_menos_3 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_3)

    # movendo o mouse para o grafico ano atual -4 e obtendo o devidendo desse ano
    pyautogui.moveTo(280, 390, 0.5, pyautogui.easeOutQuad)
    time.sleep(1)
    dividendo_ano_menos_4 = navegador.find_element(
        'xpath', '/html/body/main/div[3]/div/div[1]/div/div[3]/div/div/div[2]/span[1]').text
    print(dividendo_ano_menos_4)

    dividendo_ano_menos_1 = dividendo_ano_menos_1.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_2 = dividendo_ano_menos_2.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_3 = dividendo_ano_menos_3.replace(
        "R$ ", "").replace(",", ".")
    dividendo_ano_menos_4 = dividendo_ano_menos_4.replace(
        "R$ ", "").replace(",", ".")

    dividendo_ano_menos_1 = float(dividendo_ano_menos_1 or 0)
    dividendo_ano_menos_2 = float(dividendo_ano_menos_2 or 0)
    dividendo_ano_menos_3 = float(dividendo_ano_menos_3 or 0)
    dividendo_ano_menos_4 = float(dividendo_ano_menos_4 or 0)

    print(dividendo_ano_menos_1)
    print(dividendo_ano_menos_2)
    print(dividendo_ano_menos_3)
    print(dividendo_ano_menos_4)

    soma_dividendos = (dividendo_ano_menos_1 + dividendo_ano_menos_2 +
                       dividendo_ano_menos_3 + dividendo_ano_menos_4)

    qtde_anos = 0
    if (dividendo_ano_menos_1 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_2 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_3 > 0):
        qtde_anos = qtde_anos + 1

    if (dividendo_ano_menos_4 > 0):
        qtde_anos = qtde_anos + 1

    print(f"qtde_anos-> {qtde_anos}")
    print(f"soma_dividendos-> {soma_dividendos}")
    media_dividendos = soma_dividendos / qtde_anos
    print(f"media_dividendos-> {media_dividendos}")

    metrica_barsi = 0.06

    preco_teto = str(media_dividendos / metrica_barsi)
    preco_teto = preco_teto.replace(".", ",")

    print(f"preco_teto-> {preco_teto}")

    return preco_teto


execute()

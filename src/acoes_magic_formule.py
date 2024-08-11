# Esse bot está definido para obter dados das ações do site fundamentos e depois realizar um ranking dos melhorores
# baseados em indicadores


from utils import *

# Passo 1: importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import math
from selenium.webdriver.common.action_chains import ActionChains

ATIVO_COLUMN = 'Papel'
COTACAO_COLUMN = 'Cotação'
ROIC_COLUMN = 'ROIC'
PATRIMONIO_LIQUIDO_COLUMN = 'Liq.2meses'
EV_EBIT_COLUMN = 'EV/EBIT'
SEGMENTO_COLUMN = 'segmento'
RANK_ROIC_COLUMN = 'rank_roic'
RANK_EV_EBIT = 'rank_ev_ebit'
RANK_RESULT = 'RANK_RESULTADO'


def execute():
    # Marca o tempo de início
    inicioTempo = time.time()
    # Passo 2: requisicoes web
    navegador = openChrome()
    navegador.get("https://www.fundamentus.com.br/")

    # Passo 3: clicar no botão empresas
    botao_empresas = navegador.find_element(
        'xpath', '/html/body/div[1]/div[1]/div[1]/span/a[1]')
    navegador.execute_script("arguments[0].click();", botao_empresas)

    # Passo 4: clicar no botão buscar
    botao_buscar = navegador.find_element(
        'xpath', '/html/body/div[1]/div[2]/form/input')
    navegador.execute_script("arguments[0].click();", botao_buscar)

    # Passo 5: lendo os dados do html
    tabela_elemento = navegador.find_element(
        'xpath', '/html/body/div[1]/div[2]/table')

    html_tabela = tabela_elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]
    tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN] / 100
    print(tabela)
    tabela_customizada = tabela[[ATIVO_COLUMN,
                                COTACAO_COLUMN,
                                ROIC_COLUMN,
                                PATRIMONIO_LIQUIDO_COLUMN,
                                EV_EBIT_COLUMN,
                                 ]]

    tabela_customizada[RANK_ROIC_COLUMN] = 0.0
    tabela_customizada[RANK_EV_EBIT] = 0.0
    tabela_customizada[RANK_RESULT] = 0.0
    tabela_customizada[SEGMENTO_COLUMN] = ''

    tabela_customizada.set_index(ATIVO_COLUMN)
    # print(tabela_customizada)
#################################################################################################################
    # tratando dados
#################################################################################################################
    tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN] = formatar_valor(
        tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN])
    tabela_customizada[EV_EBIT_COLUMN] = formatar_valor(
        tabela_customizada[EV_EBIT_COLUMN])
    # print(tabela_customizada)
    # Primeiro, substitua a virgula por ponto e remova o sinal de % e converta para float
    tabela_customizada[ROIC_COLUMN] = formatar_valor_percent(
        tabela_customizada[ROIC_COLUMN])
#################################################################################################################
    # Filtros
#################################################################################################################
    tabela_filtro_liq = tabela_customizada[tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN] >= 1000000]
    tabela_filtro_dy = tabela_filtro_liq[tabela_filtro_liq[ROIC_COLUMN] > 0]
    # tabela_filtro_dy = tabela_filtro_dy[tabela_filtro_dy[EV_EBIT_COLUMN] > 0]
    # tabela_filtro_dy = tabela_filtro_dy[tabela_filtro_dy[PL_COLUMN] > 0]
    # tabela_filtro_dy = tabela_filtro_dy.head(10)

    tabela_filtro_dy = remove_tasa(tabela_filtro_dy)

    for index, row in tabela_filtro_dy.iterrows():
        ativo = row[ATIVO_COLUMN]
        print(ativo)
        baseUrl = "https://statusinvest.com.br/acoes/{}"
        baseurl = baseUrl.format(ativo)
        print(baseurl)
        navegador.get(baseurl)
        try:
            tabela_filtro_dy.at[index,
                                SEGMENTO_COLUMN] = getSegmentoEmpresa(navegador)

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=ROIC_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_ROIC_COLUMN] = tabela_filtro_dy[ROIC_COLUMN].rank(
        ascending=False)

    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=EV_EBIT_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_EV_EBIT] = tabela_filtro_dy[EV_EBIT_COLUMN].rank(
        ascending=True)

    tabela_filtro_dy[RANK_RESULT] = tabela_filtro_dy[RANK_ROIC_COLUMN] + \
        tabela_filtro_dy[RANK_EV_EBIT]
    tabela_filtro_dy = tabela_filtro_dy.sort_values(
        by=RANK_RESULT, ascending=True)
    tabela_filtro_dy["RANK_POSICAO"] = tabela_filtro_dy[RANK_RESULT].rank(
        ascending=True)

    nome_arquivo = 'acoes_magic_formule.xlsx'
    # Crie um arquivo Excel e adicione os DataFrames em abas separadas
    with pd.ExcelWriter(nome_arquivo) as writer:
        tabela_filtro_dy.to_excel(writer, sheet_name='Geral', index=False)

    # Remover repetições na coluna 'segmento'
    list_segmentos = tabela_filtro_dy[SEGMENTO_COLUMN].unique()
    # Remove os itens vazios da lista
    list_segmentos = list(filter(None, list_segmentos))
    print(f'list_segmentos: {list_segmentos}')
    # Percorrer os segmentos e cria uma abas com os dados do segmento corrente.
    for segmento in list_segmentos:
        print(f'segmento corrente: {segmento}')
        df_by_segmento = tabela_filtro_dy[tabela_filtro_dy[SEGMENTO_COLUMN] == segmento]
        print(df_by_segmento)
        with pd.ExcelWriter(nome_arquivo, mode='a') as writer:
            df_by_segmento.to_excel(
                writer, sheet_name=segmento[:30], index=False)

    print(tabela_filtro_dy)
    print(f"rows: {tabela_filtro_dy.shape[0]}")

    # Marca o tempo de término
    fimTempo = time.time()

    # Calcula o tempo decorrido
    tempo_decorrido = fimTempo - inicioTempo
    print(f"Tempo decorrido: {tempo_decorrido} segundos")


def formatar_valor(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace(
        '.', '').str.replace(',', '').astype(float) / 100

    return valor_formatado


def formatar_valor_percent(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace('.', '').str.replace(
        ',', '').str.replace('%', '').astype(float) / 100

    return valor_formatado


def format2decimal(valor):
    return float("{:.2f}".format(valor))


def getSegmentoEmpresa(navegador):
    return navegador.find_element(
        'xpath', '/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong').text


def remove_tasa(df):
    for index, row in df.iterrows():
        ativo = row[ATIVO_COLUMN]
        print(ativo)
        # removendo a tauros
        if ativo == 'TASA4':
            df = df.drop(index)
        if ativo == 'TASA3':
            df = df.drop(index)

    return df


execute()


# A formula magica no mercado de ações - Joel oWarnei yuld alterado

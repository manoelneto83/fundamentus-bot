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

ATIVO_COLUMN = 'Papel'
COTACAO_COLUMN = 'Cotação'
PVP_COLUMN = 'P/VP'
DY_COLUMN = 'Div.Yield'
ROIC_COLUMN = 'ROIC'
ROE_COLUMN = 'ROE'
PL_COLUMN = 'P/L'
PSR_COLUMN = 'PSR'
PATRIMONIO_LIQUIDO_COLUMN = 'Patrim. Líq'
VPA_COLUMN = 'vpa'
LPA_COLUMN = 'lpa'
MARGEM_LIQ_COLUMN = 'Mrg. Líq.'
MARGEM_EBIT_COLUMN = 'Mrg Ebit'
LIQ_CORRENTE_COLUMN = 'Liq. Corr.'
DIV_BRUTA_PATRIM_COLUMN = 'Dív.Brut/ Patrim.'
CRESC_RECEITA_5A = 'Cresc. Rec.5a'
GRAHAM_COLUMN = 'valor_justo_graham'
POTENCIAL_GRAHAM_COLUMN = 'potencial_graham'
EV_EBIT_COLUMN = 'EV/EBIT'
EV_EBITDA_COLUMN= 'EV/EBITDA'
P_EBIT_COLUMN = 'P/EBIT'
SEGMENTO_COLUMN = 'segmento'
RANK_DY_COLUMN = 'rank_dy'
RANK_ROE_COLUMN = 'rank_roe' 
RANK_ROIC_COLUMN = 'rank_roic' 
RANK_POTENCIAL_GRAHAM_COLUMN = 'rank_potencial_graham'
RANK_PVP_COLUMN = 'rank_pvp'
RANK_PL_COLUMN = 'rank_pl'
RANK_MARGEM_LIQ = 'rank_margem_liq'
RANK_DIV_BRUTA_PATRIM = 'rank_div_bruta_patrim'
RANK_CRESC_RECEITA_5A = 'rank_cresc_receita_5a'
RANK_LIQ_CORRENTE = 'rank_liq_corrente'
RANK_MARGEM_EBIT = 'rank_margem_ebit'
RANK_EV_EBIT = 'rank_ev_ebit'
RANK_EV_EBITDA = 'rank_ev_ebitda'
RANK_P_EBIT = 'rank_p_ebit'
RANK_RESULT = 'RANK_RESULTADO'


# SEGMENTOS
# Híbrido
# Lajes Corporativas
# Logística
# Outros
# Shoppings
# Títulos e Val. Mob.


def execute():
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
    tabela[COTACAO_COLUMN] = tabela[COTACAO_COLUMN]/ 100
    tabela[LIQ_CORRENTE_COLUMN] = tabela[LIQ_CORRENTE_COLUMN]/ 100
    tabela[DIV_BRUTA_PATRIM_COLUMN] = tabela[DIV_BRUTA_PATRIM_COLUMN]/ 100
    # tabela[EV_EBIT_COLUMN] = tabela[EV_EBIT_COLUMN]/ 100
    # tabela[EV_EBITDA_COLUMN] = tabela[EV_EBITDA_COLUMN]/ 100
    # tabela[P_EBIT_COLUMN] = tabela[P_EBIT_COLUMN]/ 100
    print(tabela)
    tabela_customizada = tabela[[ATIVO_COLUMN,
                                COTACAO_COLUMN,
                                PL_COLUMN,
                                DY_COLUMN,
                                PVP_COLUMN,
                                ROIC_COLUMN,
                                ROE_COLUMN,
                                PATRIMONIO_LIQUIDO_COLUMN,
                                PSR_COLUMN,
                                MARGEM_EBIT_COLUMN,
                                MARGEM_LIQ_COLUMN,
                                LIQ_CORRENTE_COLUMN,
                                DIV_BRUTA_PATRIM_COLUMN,
                                CRESC_RECEITA_5A,
                                EV_EBIT_COLUMN,
                                EV_EBITDA_COLUMN,
                                P_EBIT_COLUMN
                                ]]

    tabela_customizada[VPA_COLUMN] = 0.0
    tabela_customizada[LPA_COLUMN] = 0.0
    tabela_customizada[GRAHAM_COLUMN] = 0.0
    tabela_customizada[POTENCIAL_GRAHAM_COLUMN] = 0.0
    tabela_customizada[RANK_DY_COLUMN] = 0.0
    tabela_customizada[RANK_ROE_COLUMN] = 0.0
    tabela_customizada[RANK_ROIC_COLUMN] = 0.0
    tabela_customizada[RANK_POTENCIAL_GRAHAM_COLUMN] = 0.0
    tabela_customizada[RANK_PVP_COLUMN] = 0.0
    tabela_customizada[RANK_PL_COLUMN] = 0.0
    tabela_customizada[RANK_MARGEM_LIQ] = 0.0
    tabela_customizada[RANK_CRESC_RECEITA_5A] = 0.0
    tabela_customizada[RANK_DIV_BRUTA_PATRIM] = 0.0
    tabela_customizada[RANK_LIQ_CORRENTE] = 0.0
    tabela_customizada[RANK_MARGEM_EBIT] = 0.0
    tabela_customizada[RANK_EV_EBIT] = 0.0
    tabela_customizada[RANK_EV_EBITDA] = 0.0
    tabela_customizada[RANK_P_EBIT] = 0.0

    tabela_customizada[RANK_RESULT] = 0.0
    tabela_customizada[SEGMENTO_COLUMN] = ''

    
    tabela_customizada.set_index(ATIVO_COLUMN)
    # print(tabela_customizada)
    # Primeiro, remova os pontos da coluna de liquidez e converta para float
    tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN] = formatar_valor(tabela_customizada[PATRIMONIO_LIQUIDO_COLUMN])
    tabela_customizada[PL_COLUMN] = formatar_valor(tabela_customizada[PL_COLUMN])
    tabela_customizada[PSR_COLUMN] = formatar_valor(tabela_customizada[PSR_COLUMN])
    tabela_customizada[EV_EBIT_COLUMN] = formatar_valor(tabela_customizada[EV_EBIT_COLUMN])
    tabela_customizada[EV_EBITDA_COLUMN] = formatar_valor(tabela_customizada[EV_EBITDA_COLUMN])
    tabela_customizada[P_EBIT_COLUMN] = formatar_valor(tabela_customizada[P_EBIT_COLUMN])
    # print(tabela_customizada)
    # Primeiro, substitua a virgula por ponto e remova o sinal de % e converta para float
    tabela_customizada[DY_COLUMN] = formatar_valor_percent(tabela_customizada[DY_COLUMN])
    tabela_customizada[ROIC_COLUMN] = formatar_valor_percent(tabela_customizada[ROIC_COLUMN])
    tabela_customizada[ROE_COLUMN] = formatar_valor_percent(tabela_customizada[ROE_COLUMN])
    tabela_customizada[MARGEM_EBIT_COLUMN] = formatar_valor_percent(tabela_customizada[MARGEM_EBIT_COLUMN])
    tabela_customizada[MARGEM_LIQ_COLUMN] = formatar_valor_percent(tabela_customizada[MARGEM_LIQ_COLUMN])
    tabela_customizada[CRESC_RECEITA_5A] = formatar_valor_percent(tabela_customizada[CRESC_RECEITA_5A])


    # Filtros
    tabela_filtro_pvp = tabela_customizada[tabela_customizada[PVP_COLUMN] <= 900]
    tabela_filtro_roe = tabela_filtro_pvp[tabela_filtro_pvp[ROE_COLUMN] >= 13]
    tabela_filtro_roic = tabela_filtro_roe[tabela_filtro_roe[ROIC_COLUMN] >= 0]

    # ALGUNS SETORES COMO O BANCARIO TEM O PSR = 0
    tabela_filtro_psr = tabela_filtro_roic[tabela_filtro_roic[PSR_COLUMN] >= 0]
    # tabela_filtro_dy = tabela_filtro_roic[tabela_filtro_roic[DY_COLUMN] >= 4]

    # ALGUNS SETORES COMO BANCARIOS E SEGUROS TEM ESSE INDICADOR = 0
    tabela_filtro_margem_liq = tabela_filtro_psr[tabela_filtro_psr[MARGEM_LIQ_COLUMN] >= 0]
    tabela_filtro_margem_ebit = tabela_filtro_margem_liq[tabela_filtro_margem_liq[MARGEM_EBIT_COLUMN] >= 0]
    tabela_filtro_p_ebit = tabela_filtro_margem_ebit[tabela_filtro_margem_ebit[P_EBIT_COLUMN] <= 10]

    tabela_filtro_dy = tabela_filtro_p_ebit[tabela_filtro_p_ebit[DY_COLUMN] >= 4]

    # tabela_filtro_dy = tabela_filtro_dy.head(10)

    for index, row in tabela_filtro_dy.iterrows():
        ativo = row[ATIVO_COLUMN]
        print(ativo)
        # navegador = openChrome()
        baseUrl = "https://statusinvest.com.br/acoes/{}"
        baseurl = baseUrl.format(ativo)
        print(baseurl)
        navegador.get(baseurl)
        try:
            preco_justo = float(preco_justo_graham(navegador, index, tabela_filtro_dy))
            # print(f"preco_justo-> {preco_justo}")
            # print(f"preco_justo type-> {type(preco_justo)}")
            # print(f"cotacao -> {row['Cotação']}")
            # print(f"cotacao type -> {type(row['Cotação'])}")
            # print(f"calculo -> {(preco_justo/row['Cotação'])}")
            tabela_filtro_dy.at[index, SEGMENTO_COLUMN] = getSegmentoEmpresa(navegador)
            tabela_filtro_dy.at[index, GRAHAM_COLUMN] = preco_justo
            potencial = ((preco_justo/row[COTACAO_COLUMN])*100)-100
            tabela_filtro_dy.at[index, POTENCIAL_GRAHAM_COLUMN] = format2decimal(potencial)

        except Exception as err:
            imprimir(f"Ocorreu um erro: {err}")
            tabela_filtro_dy.at[index, GRAHAM_COLUMN] = 0
            tabela_filtro_dy.at[index, POTENCIAL_GRAHAM_COLUMN] = 0

    print(f"potencial type -> {type(row[POTENCIAL_GRAHAM_COLUMN])}")

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=DY_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_DY_COLUMN] = tabela_filtro_dy[DY_COLUMN].rank(ascending=False)    

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=ROE_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_ROE_COLUMN] = tabela_filtro_dy[ROE_COLUMN].rank(ascending=False)   

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=ROIC_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_ROIC_COLUMN] = tabela_filtro_dy[ROIC_COLUMN].rank(ascending=False)   

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=POTENCIAL_GRAHAM_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_POTENCIAL_GRAHAM_COLUMN] = tabela_filtro_dy[POTENCIAL_GRAHAM_COLUMN].rank(ascending=False)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=LIQ_CORRENTE_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_LIQ_CORRENTE] = tabela_filtro_dy[LIQ_CORRENTE_COLUMN].rank(ascending=False)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=MARGEM_LIQ_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_MARGEM_LIQ] = tabela_filtro_dy[MARGEM_LIQ_COLUMN].rank(ascending=False)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=CRESC_RECEITA_5A, ascending=False)
    tabela_filtro_dy[RANK_CRESC_RECEITA_5A] = tabela_filtro_dy[CRESC_RECEITA_5A].rank(ascending=False)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=MARGEM_EBIT_COLUMN, ascending=False)
    tabela_filtro_dy[RANK_MARGEM_EBIT] = tabela_filtro_dy[MARGEM_EBIT_COLUMN].rank(ascending=False)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=PVP_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_PVP_COLUMN] = tabela_filtro_dy[PVP_COLUMN].rank(ascending=True)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=PL_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_PL_COLUMN] = tabela_filtro_dy[PL_COLUMN].rank(ascending=True)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=DIV_BRUTA_PATRIM_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_DIV_BRUTA_PATRIM] = tabela_filtro_dy[DIV_BRUTA_PATRIM_COLUMN].rank(ascending=True)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=EV_EBIT_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_EV_EBIT] = tabela_filtro_dy[EV_EBIT_COLUMN].rank(ascending=True)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=EV_EBITDA_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_EV_EBITDA] = tabela_filtro_dy[EV_EBITDA_COLUMN].rank(ascending=True)  

    tabela_filtro_dy = tabela_filtro_dy.sort_values(by=P_EBIT_COLUMN, ascending=True)
    tabela_filtro_dy[RANK_P_EBIT] = tabela_filtro_dy[P_EBIT_COLUMN].rank(ascending=True)  

    tabela_filtro_dy[RANK_RESULT]  = tabela_filtro_dy[RANK_DY_COLUMN] + tabela_filtro_dy[RANK_ROE_COLUMN] + tabela_filtro_dy[RANK_ROIC_COLUMN] + tabela_filtro_dy[RANK_POTENCIAL_GRAHAM_COLUMN] + tabela_filtro_dy[RANK_PVP_COLUMN] + tabela_filtro_dy[RANK_PL_COLUMN] + tabela_filtro_dy[RANK_LIQ_CORRENTE] + tabela_filtro_dy[RANK_MARGEM_LIQ] + tabela_filtro_dy[RANK_CRESC_RECEITA_5A] + tabela_filtro_dy[RANK_DIV_BRUTA_PATRIM] + tabela_filtro_dy[RANK_MARGEM_EBIT] + tabela_filtro_dy[RANK_EV_EBIT] + tabela_filtro_dy[RANK_EV_EBITDA] + tabela_filtro_dy[P_EBIT_COLUMN]
    nome_arquivo_csv = 'meu_dataframe_acoes.csv'

    # # # Use o método to_csv para exportar o DataFrame para um arquivo CSV
    tabela_filtro_dy.to_csv(nome_arquivo_csv, index=False,  decimal=',')

    print(tabela_filtro_dy)
    print(f"rows: {tabela_filtro_dy.shape[0]}")



def formatar_valor(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace('.', '').str.replace(',', '').astype(float) / 100
    
    return valor_formatado

def formatar_valor_percent(valor):
    # Remove todos os pontos e vírgulas da string
    valor_formatado = valor.str.replace('.', '').str.replace(',', '').str.replace('%', '').astype(float) / 100
    
    return valor_formatado

def preco_justo_graham(navegador, index, tabela_filtro_dy):
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

    tabela_filtro_dy.at[index, VPA_COLUMN] = vpa
    tabela_filtro_dy.at[index, LPA_COLUMN] = lpa

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
    valor_formatado = format2decimal(raiz)
    print(f"raiz valor_formatado -> {valor_formatado}") 
    return valor_formatado

def format2decimal(valor):
    return float("{:.2f}".format(valor))

def getSegmentoEmpresa(navegador):
        return navegador.find_element(
        'xpath', '/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong').text

    

execute()


# A formula magica no mercado de ações - Joel oWarnei yuld alterado


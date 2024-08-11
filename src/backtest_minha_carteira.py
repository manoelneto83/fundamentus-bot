# Passo 1: importando as libs
import pandas as pd
import quantstats as qs
import time


# lendo os dados
dados_empresas = pd.read_csv('dados_empresas.csv')

# filtro
# PRA SEMPRE -
ativos_desejados = ['VALE3', 'TAEE11', 'TRPL4',
                    'CMIG4', 'CXSE3', 'KLBN4', 'PETR4', 'BBSE3', 'SARP11', 'BBSA3']

# 18/05/2024 325,51
# ativos_desejados = ['AURE3', 'VALE3', 'TAEE11', 'TRPL4', 'JALL3', 'GOAU4',
#                     'CSAN3', 'CMIG4', 'CXSE3', 'KLBN4', 'PETR4', 'BBSE3', 'SARP11', 'BBSA3']

# MINHA CARTEIRA (HOJE) - 369,80
# ativos_desejados = ['TAEE11', 'TRPL4','VALE3', 'GOAU4', 'CMIG4', 'PETR4', 'CXSE3', 'KLBN4', 'POSI3', 'CBAV3', 'TASA3', 'TASA4', 'BMGB4', 'SAPR11', 'BBAS3', 'VIVT3', 'USIM5', 'CMIN3', 'TAEE4', 'ITUB4', 'TECN3', 'MRFG3', 'RANI3', 'ITSA4']

# PRA SEMPRE + MAGIC_FORMULE (MEU DEDO) - 942,69
# ativos_desejados = ['TAEE11', 'TRPL4','CMIG4', 'KLBN4', 'SARP11', 'BBSA3', 'PETR4', 'VALE3', 'BBSE3', 'UNIP6',
# 'GOAU4', 'FESA4', 'KEPL3', 'RECV3', 'WIZC3']

# PRA SEMPRE + MAGIC_FORMULE (JOE) 901,84
# ativos_desejados = ['TAEE11', 'TRPL4','CMIG4', 'KLBN4', 'SARP11', 'BBSA3', 'PETR4', 'VALE3', 'BBSE3', 'UNIP6',
# 'PSSA3', 'CAMB3', 'KEPL3', 'VLID3', 'WIZC3']

# PRA SEMPRE + MAGIC_FORMULE + BAZIN + GRAHAM - 673,93
# ativos_desejados = ['TAEE11', 'TRPL4','CMIG4', 'KLBN4', 'SARP11', 'BBSA3', 'PETR4', 'VALE3', 'BBSE3', 'UNIP6',
# 'GOAU4', 'WIZC3', 'VLID3', 'AURA33', 'KEPL3']

filtro = dados_empresas['ticker'].isin(ativos_desejados)
dados_empresas = dados_empresas[filtro]

dados_empresas = dados_empresas[dados_empresas['volume_negociado'] > 1000000]

# calculando o retorno de cada acao no mês
dados_empresas['retorno'] = dados_empresas.groupby(
    'ticker')['preco_fechamento_ajustado'].pct_change()
dados_empresas['retorno'] = dados_empresas['retorno'].shift(-1)

dados_empresas['rank_ebit_ev'] = dados_empresas.groupby(
    'data')['ebit_ev'].rank(ascending=False)
dados_empresas['rank_roic'] = dados_empresas.groupby(
    'data')['roic'].rank(ascending=False)
dados_empresas['rank_final'] = dados_empresas['rank_ebit_ev'] + \
    dados_empresas['rank_roic']
dados_empresas['rank_final'] = dados_empresas.groupby(
    'data')['rank_final'].rank(ascending=True)
dados_empresas = dados_empresas.sort_values(by='rank_final', ascending=True)

# dados_empresas = dados_empresas[dados_empresas['data'] == '2012-12-31']

# criar a carteira
dados_empresas = dados_empresas[dados_empresas['rank_final'] <= 10]
# dados_empresas = dados_empresas.head(10)

print(dados_empresas)

# calcular a rentabilidade da carteira
rentabilidade_por_carteira = dados_empresas.groupby('data')['retorno'].mean()

rentabilidade_por_carteira = rentabilidade_por_carteira.to_frame()

# calcular a rentabilidade do modelo
rentabilidade_por_carteira['retorno'] = (
    rentabilidade_por_carteira['retorno'] + 1).cumprod() - 1

rentabilidade_por_carteira['retorno'] = rentabilidade_por_carteira['retorno'].shift(
    1)
rentabilidade_por_carteira = rentabilidade_por_carteira.dropna()

print(rentabilidade_por_carteira)

# calcular a rentabilidade do ibovespa no mesmo periodo

ibov = pd.read_csv('ibov.csv')
retornos_ibov = ibov['fechamento'].pct_change().dropna()

print(retornos_ibov)

retornos_ibov = (retornos_ibov + 1).cumprod() - 1

print(retornos_ibov)

rentabilidade_por_carteira['ibovespa'] = retornos_ibov.values

print(rentabilidade_por_carteira)

# analisar os dados

qs.extend_pandas()

rentabilidade_por_carteira.index = pd.to_datetime(
    rentabilidade_por_carteira.index)

print(rentabilidade_por_carteira)

qs.plots.monthly_heatmap(
    rentabilidade_por_carteira['retorno'], savefig="rentabilidade_por_carteira", show=True)
qs.plots.monthly_heatmap(
    rentabilidade_por_carteira['ibovespa'], savefig="ibovespa", show=True)

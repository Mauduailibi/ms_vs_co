import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import locale
import os
from PIL import Image

locale.setlocale( locale.LC_ALL, 'pt_BR.UTF-8' )
dirname = os.path.dirname(__file__)

image_bandeira = Image.open('./assets/img/bandeira_ms.png')
image_mapa = Image.open('./assets/img/ms_no_mapa.png')
image_bonito = Image.open('./assets/img/bonito.jpg')
imagem_campo_grande = Image.open('./assets/img/campo_grande.jpg')
imagem_corumba = Image.open('./assets/img/corumba.jpg')
imagem_boiada = Image.open('./assets/img/boiada.jpg')

tabela_pib = pd.read_excel('./assets/xls/tabela.xlsx', 'Produto Interno Bruto 2007')
tabela_pop = pd.read_excel('./assets/xls/tabela.xlsx', 'População Domicílios Censo 2000')
tabela_pec = pd.read_excel('./assets/xls/tabela.xlsx', 'Pecuária 2008')
tabela_agro = pd.read_excel('./assets/xls/tabela.xlsx', 'Produção Agrícola 2007')
tabela_homicidios = pd.read_excel('./assets/xls/tabela.xlsx', 'SIM-obitos e homicidios')

def f(d):
    return '{0:n}'.format(d)

def reais(f):
    return locale.currency(f, grouping=True, symbol=True)

def til(s):
    return s.replace('Ò', 'ã')

# Título e descrição

st.sidebar.image(image_bandeira, use_column_width=True, caption='Bandeira do Mato Grosso do Sul')
st.sidebar.image(image_mapa, use_column_width=True, caption='Mato Grosso do Sul no mapa do Brasil')
st.sidebar.image(image_bonito, use_column_width=True, caption='Águas cristalinas de Bonito')
st.sidebar.image(imagem_corumba, use_column_width=True, caption='Cidade de Corumbá ao longo do Rio Paraguai')
st.sidebar.image(imagem_boiada, use_column_width=True, caption='Boiada atravessando o Pantanal alagado')
st.sidebar.write('')

st.title('Mato Grosso do Sul')

st.write('Mato Grosso do Sul é uma das 27 unidades federativas do Brasil. Localiza-se no sul da Região Centro-Oeste. Limita-se com cinco estados brasileiros: Mato Grosso (norte), Goiás e Minas Gerais (nordeste), São Paulo (leste) e Paraná (sudeste); e dois países sul-americanos: Paraguai (sul e sudoeste) e Bolívia (oeste). É dividido em 79 municípios e ocupa uma área é de 357 145,532 km², com tamanho comparável à Alemanha. Com uma população de 2 839 188 habitantes em 2021, Mato Grosso do Sul é o 21º estado mais populoso do Brasil.')

st.image(imagem_campo_grande, use_column_width=True, caption='Vista da cidade de Campo Grande, cidade mais bonita do Brasil')

st.header('MS vs Centro Oeste vs Brasil')
st.write('Vamos analisar os dados do estado do Mato Grosso do Sul ante a região Centro-Oeste e o Brasil. Os dados analisados serão: Produto Interno Bruto, População, Pecuária e Produção Agrícola.')
st.caption('Todos os dados analisados aconteceram entre os anos 2000 e 2009, sendo analisados apenas os dados do ano vigente na legenda e não de todo o período.')
st.caption('As análises de estados individuais não consideram o Distrito Federal.')

tab_pib, tab_pop, tab_hom, tab_pec, tab_agro = st.tabs(['PIB', 'População', 'Homicídios', 'Pecuária', 'Produção Agrícola'])

# Fim da descrição

# Cálculos de PIB

soma_pib_brasil = 0
soma_pib_ms = 0
soma_pib_co = 0

pib_ms_agro = 0
pib_ms_ind = 0
pib_ms_serv = 0
pib_ms_imp = 0

pib_br_agro = 0
pib_br_ind = 0
pib_br_serv = 0
pib_br_imp = 0

for idx, val in enumerate(tabela_pib['Código IBGE da unidade da federação']):
    soma_pib_brasil += tabela_pib.iloc[idx]['PIB a preços correntes']
    pib_br_agro += tabela_pib.iloc[idx]['Valor adicionado bruto da agropecuária']
    pib_br_ind += tabela_pib.iloc[idx]['Valor adicionado bruto da indústria']
    pib_br_serv += tabela_pib.iloc[idx]['Valor adicionado bruto dos serviços']
    pib_br_imp += tabela_pib.iloc[idx]['Impostos sobre produtos líquidos de subsídios']
    
    if val == 'MS' :
        soma_pib_ms += tabela_pib.iloc[idx]['PIB a preços correntes']
        pib_ms_agro += tabela_pib.iloc[idx]['Valor adicionado bruto da agropecuária']
        pib_ms_ind += tabela_pib.iloc[idx]['Valor adicionado bruto da indústria']
        pib_ms_serv += tabela_pib.iloc[idx]['Valor adicionado bruto dos serviços']
        pib_ms_imp += tabela_pib.iloc[idx]['Impostos sobre produtos líquidos de subsídios']

    if tabela_pop.iloc[idx]['Grandes regiões'] == 'Centro-Oeste':
        soma_pib_co += tabela_pib.iloc[idx]['PIB a preços correntes']

soma_pib_ms *= 1000
soma_pib_co *= 1000
soma_pib_brasil *= 1000

pib_ms = locale.currency(soma_pib_ms, grouping=True, symbol=True)
pib_co = locale.currency(soma_pib_co, grouping=True, symbol=True)
pib_brasil = locale.currency(soma_pib_brasil, grouping=True, symbol=True)

# Gráficos composição do PIB

x = [pib_ms_agro, pib_ms_ind, pib_ms_serv, pib_ms_imp];
colors = plt.get_cmap('plasma')(np.linspace(0.2, 0.7, len(x)))

figCompPibMS, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Agropecuária', 'Indústria', 'Serviços', 'Impostos'])

x = [pib_br_agro, pib_br_ind, pib_br_serv, pib_br_imp];
colors = plt.get_cmap('plasma')(np.linspace(0.2, 0.7, len(x)))

figCompPibBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Agropecuária', 'Indústria', 'Serviços', 'Impostos'])

# Gráficos de PIB

x = [soma_pib_ms, soma_pib_co];
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

figPibMSCO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Centro-Oeste'])

x = [soma_pib_ms, soma_pib_brasil];
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

figPibMSBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Brasil'])

# Fim dos cálculos de PIB

# Início dos cálculos de PIB per capita

pib_per_capita_municipios = list()
municipios = list()
ppc_cg = 0
ppc_max = 0

for idx, val in enumerate(tabela_pib['Código IBGE da unidade da federação']):
    if val == 'MS' :
        pib_per_capita_municipios.append(tabela_pib.iloc[idx]['PIB per capita'])
        municipios.append(tabela_pib.iloc[idx]['Nome do município'])
    
    if tabela_pib.iloc[idx]['Nome do município'] == 'Campo Grande':
        ppc_cg = tabela_pib.iloc[idx]['PIB per capita']

ppc_max = max(pib_per_capita_municipios)
idx_ppc_max = pib_per_capita_municipios.index(ppc_max)

ppc_min = min(pib_per_capita_municipios)
idx_ppc_min = pib_per_capita_municipios.index(ppc_min)

figPPCMS, ax = plt.subplots()
ax.hist(pib_per_capita_municipios, 5, rwidth=0.9)

# Fim dos cálculos de PIB per capita

# Início dos cálculos de população

pop_ms = 0;
pop_co = 0;
pop_brasil = 0;

for idx, val in enumerate(tabela_pop['Código IBGE da unidade da federação']):
    pop_brasil += tabela_pop.iloc[idx]['Pessoas residentes - resultados da amostra - municípios vigentes em 2001']
    
    if val == 'MS' :
        pop_ms += tabela_pop.iloc[idx]['Pessoas residentes - resultados da amostra - municípios vigentes em 2001']
    if tabela_pop.iloc[idx]['Grandes regiões'] == 'Centro-Oeste':
        pop_co += tabela_pop.iloc[idx]['Pessoas residentes - resultados da amostra - municípios vigentes em 2001']

x = [pop_ms, pop_co];
colors = plt.get_cmap('Reds')(np.linspace(0.2, 0.7, len(x)))

figPopMSCO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Centro-Oeste'])

x = [pop_ms, pop_brasil];
colors = plt.get_cmap('Reds')(np.linspace(0.2, 0.7, len(x)))

figPopMSBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Brasil'])

# Fim dos cálculos de população

# Início dos cálculos da pecuária

bovinos_ms = 0
bovinos_co = 0
bovinos_brasil = 0

bovinos_mt = 0
bovinos_go = 0

for idx, val in enumerate(tabela_pec['Código IBGE da unidade da federação']):
    bovinos_brasil += tabela_pec.iloc[idx]['Bovinos - efetivo dos rebanhos']

    if val == 'MS' :
        bovinos_ms += tabela_pec.iloc[idx]['Bovinos - efetivo dos rebanhos']
    if val == 'MT' :
        bovinos_mt += tabela_pec.iloc[idx]['Bovinos - efetivo dos rebanhos']
    if val == 'GO' :
        bovinos_go += tabela_pec.iloc[idx]['Bovinos - efetivo dos rebanhos']

    if tabela_pec.iloc[idx]['Grandes regiões'] == 'Centro-Oeste':
        bovinos_co += tabela_pec.iloc[idx]['Bovinos - efetivo dos rebanhos']

# Gráficos de pecuária

x = [bovinos_ms, bovinos_mt, bovinos_go];
colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(x)))

figPecMSMTGO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Mato Grosso', 'Goiás'])

x = [bovinos_ms, bovinos_co];
colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(x)))

figPecMSCO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Centro-Oeste'])

x = [bovinos_ms, bovinos_brasil];
colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(x)))

figPecMSBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Brasil'])

# Fim dos cálculos da pecuária

# Início dos cálculos da produção agrícola

soja_ms = 0
soja_co = 0
soja_brasil = 0

soja_mt = 0
soja_go = 0
milho_mt = 0
milho_go = 0

milho_ms = 0
milho_co = 0
milho_brasil = 0

for idx, val in enumerate(tabela_agro['Código IBGE da unidade da federação']):
    soja_brasil += tabela_agro.iloc[idx]['Soja (em grão) - Quantidade produzida']
    milho_brasil += tabela_agro.iloc[idx]['Milho (em grão) - Quantidade produzida']

    if val == 'MS':
        soja_ms += tabela_agro.iloc[idx]['Soja (em grão) - Quantidade produzida']
        milho_ms += tabela_agro.iloc[idx]['Milho (em grão) - Quantidade produzida']
    if val == 'MT':
        soja_mt += tabela_agro.iloc[idx]['Soja (em grão) - Quantidade produzida']
        milho_mt += tabela_agro.iloc[idx]['Milho (em grão) - Quantidade produzida']
    if val == 'GO':
        soja_go += tabela_agro.iloc[idx]['Soja (em grão) - Quantidade produzida']
        milho_go += tabela_agro.iloc[idx]['Milho (em grão) - Quantidade produzida']

    if tabela_agro.iloc[idx]['Grandes regiões'] == 'Centro-Oeste':
        soja_co += tabela_agro.iloc[idx]['Soja (em grão) - Quantidade produzida']
        milho_co += tabela_agro.iloc[idx]['Milho (em grão) - Quantidade produzida']

# Gráficos de produção agrícola
# Soja

x = [soja_ms, soja_mt, soja_go];
colors = plt.get_cmap('Purples')(np.linspace(0.2, 0.7, len(x)))

figSojaMSMTGO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Mato Grosso', 'Goiás'])

x = [soja_ms, soja_co];
colors = plt.get_cmap('Purples')(np.linspace(0.2, 0.7, len(x)))

figSojaMSCO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Centro-Oeste'])

x = [soja_ms, soja_brasil];
colors = plt.get_cmap('Purples')(np.linspace(0.2, 0.7, len(x)))

figSojaMSBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Brasil'])

# Milho

x = [milho_ms, milho_mt, milho_go];
colors = plt.get_cmap('summer')(np.linspace(0.2, 0.7, len(x)))

figMilhoMSMTGO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Mato Grosso', 'Goiás'])

x = [milho_ms, milho_co];
colors = plt.get_cmap('summer')(np.linspace(0.2, 0.7, len(x)))

figMilhoMSCO, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Centro-Oeste'])

x = [milho_ms, milho_brasil];
colors = plt.get_cmap('summer')(np.linspace(0.2, 0.7, len(x)))

figMilhoMSBR, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 3, "edgecolor": "white"}, frame=False)

ax.legend(['Mato Grosso do Sul', 'Brasil'])

# Fim dos cálculos da produção agrícola

# Início dos cálculos de homicídios

homicidios_2009 = list()
homicidios_2008 = list()
homicidios_2007 = list()
municipios_homicidios = list()

for idx, val in enumerate(tabela_homicidios['C_digo_IBGE_da_unidade_da_federa']):

    if val == 'MS':
        mun_pop = tabela_homicidios.iloc[idx]['Pessoas_residentes___resultados_']
        homicidios_totais_2009 = tabela_homicidios.iloc[idx]['homicidios2009']
        homicidios_totais_2008 = tabela_homicidios.iloc[idx]['homicidios2008']
        homicidios_totais_2007 = tabela_homicidios.iloc[idx]['homicidios2007']

        homicidios_2009.append(round(homicidios_totais_2009 / mun_pop * 100000, 1))
        homicidios_2008.append(round(homicidios_totais_2008 / mun_pop * 100000, 1))
        homicidios_2007.append(round(homicidios_totais_2007 / mun_pop * 100000, 1))
        municipios_homicidios.append(tabela_homicidios.iloc[idx]['Nome_do_munic_pio'])

homicidios_municipios = np.array([homicidios_2009, homicidios_2008, homicidios_2007])
homicidios_municipios_title = np.array([municipios_homicidios, homicidios_2009, homicidios_2008, homicidios_2007])

figHomicidiosMS = px.box(homicidios_municipios.transpose())

# Fim dos cálculos de homicídios

# Início das tabs

with tab_pib:
    st.header('Produto Interno Bruto - 2007')
    st.write('O PIB é a soma de todos os bens e serviços finais produzidos por um país, estado ou cidade, geralmente em um ano. Todos os países calculam o seu PIB nas suas respectivas moedas. O PIB do Brasil em 2021, por exemplo, foi de R$ 8,7 trilhões.')

    pib_col1, pib_spc, pib_col2 = st.columns([3, 1, 3])

    with pib_col1:
        st.subheader('Composição PIB MS')
        st.pyplot(figCompPibMS)
        st.write('Agropecuária: ', reais(pib_ms_agro))
        st.write('Indústria:', reais(pib_ms_ind))
        st.write('Serviços:', reais(pib_ms_serv))
        st.write('Impostos:', reais(pib_ms_imp))

    with pib_col2:
        st.subheader('Composição PIB Brasil')
        st.pyplot(figCompPibBR)
        st.write('Agropecuária: ', reais(pib_br_agro))
        st.write('Indústria:', reais(pib_br_ind))
        st.write('Serviços:', reais(pib_br_serv))
        st.write('Impostos:', reais(pib_br_imp))


    pib_col1, pib_spc, pib_col2 = st.columns([3, 1, 3])

    pib_ms_co_perc = round((soma_pib_ms / soma_pib_co) * 100, 2)
    pib_ms_brasil_perc = round((soma_pib_ms / soma_pib_brasil) * 100, 2)

    with pib_col1:
        st.subheader('MS vs Centro Oeste')
        st.pyplot(figPibMSCO)
        st.write('PIB MS: ', pib_ms)
        st.write('PIB Centro-oeste: ', pib_co)
        st.write('Representa ', str(pib_ms_co_perc), '% do PIB do Centro-oeste')

    with pib_col2:
        st.subheader('MS vs Brasil')
        st.pyplot(figPibMSBR)
        st.write('PIB MS: ', pib_ms)
        st.write('PIB Brasil: ', pib_brasil)
        st.write('Representa ', str(pib_ms_brasil_perc), '% do PIB do Brasil')

    pib_col1, pib_col2 = st.columns([3, 1])

    with pib_col1:
        st.subheader('PIB per capita - Municípios do MS')
        st.pyplot(figPPCMS)
        st.write('PIB per capita Campo Grande: ', reais(ppc_cg))
        st.write('PIB per máximo: ', reais(ppc_max), ' - município de ', til(municipios[idx_ppc_max]))
        st.write('PIB per mínimo: ', reais(ppc_min), ' - município de ', til(municipios[idx_ppc_min]))


with tab_pop:
    st.header('População - Censo de 2000 (IBGE)')
    st.write('Segundo o Censo de 2000 do IBGE, a população brasileira era de aproximadamente 169 milhões de habitantes. Nessa mesma contagem, a população do estado do Mato Grosso do Sul era de aproximadamente 2 milhões de habitantes, enquanto a da região Centro-Oeste era de 11,5 milhões de pessoas. As análises podem ser observadas nos gráficos abaixo.')

    pop_col1, pop_spc, pop_col2 = st.columns([3, 1, 3])

    pop_ms_co_perc = round((pop_ms / pop_co) * 100, 2)
    pop_ms_brasil_perc = round((pop_ms / pop_brasil) * 100, 2)

    with pop_col1:
        st.subheader('MS vs Centro Oeste')
        st.pyplot(figPopMSCO)
        st.write('População MS: ', f(pop_ms))
        st.write('População Centro-oeste: ', f(pop_co))
        st.write('Representa ', str(pop_ms_co_perc), '% da população do Centro-oeste')

    with pop_col2:
        st.subheader('MS vs Brasil')
        st.pyplot(figPopMSBR)
        st.write('População MS: ', f(pop_ms))
        st.write('População Brasil: ', f(pop_brasil))
        st.write('Representa ', str(pop_ms_brasil_perc), '% da população do Brasil')

with tab_hom:
    st.header('Homicídios - 2009, 2008, 2007')
    st.write('Os homicídios são crimes que resultam em morte de uma pessoa por outra. A análise dos homicídios no estado do Mato Grosso do Sul por município pode ser observada nos gráficos abaixo. Lembrando que os dados estão classificados em taxa por 100 mil habitantes.')

    st.plotly_chart(figHomicidiosMS)

with tab_pec:
    st.header('Pecuária 2008 - Total de bovinos')
    st.write('Nos gráficos abaixo é possível observar a distribuição da quantidade de bovinos no Mato Grosso do Sul, Centro-Oeste e Brasil, e a relação entre eles. Diferente das últimas áreas de observação, onde os números do MS representava cerca de 10% do Centro-Oeste e 1% em nível de Brasil, quando se fala em bovinos, o MS representava mais de 30% do número total de cabeças do Centro-Oeste e 11% do total no Brasil.')

    pec_col1, pec_spc, pec_col2 = st.columns([3, 1, 3])

    pec_ms_co_perc = round((bovinos_ms / bovinos_co) * 100, 2)
    pec_ms_brasil_perc = round((bovinos_ms / bovinos_brasil) * 100, 2)

    with pec_col1:
        st.subheader('MS vs Centro Oeste')
        st.pyplot(figPecMSCO)
        st.write('Total de bovinos MS: ', f(bovinos_ms))
        st.write('Total de bovinos Centro-oeste: ', f(bovinos_co))
        st.write('Representa ', str(pec_ms_co_perc), '% dos bovinos do Centro-oeste')

    with pec_col2:
        st.subheader('MS vs Brasil')
        st.pyplot(figPecMSBR)
        st.write('Total de bovinos MS: ', f(bovinos_ms))
        st.write('Total de bovinos Brasil: ', f(bovinos_brasil))
        st.write('Representa ', str(pec_ms_brasil_perc), '% dos bovinos do Brasil')

    pec_col1, pec_spc, pec_col2 = st.columns([3, 1, 3])

    with pec_col1:
        st.subheader('MS vs MT vs GO')
        st.pyplot(figPecMSMTGO)
        st.write('Total de bovinos MS: ', f(bovinos_ms))
        st.write('Total de bovinos MT: ', f(bovinos_mt))
        st.write('Total de bovinos GO: ', f(bovinos_go))


with tab_agro:
    st.header('Produção agrícola 2007')
    st.write('Os gráficos abaixo representam as produções agrículas de soja e milho do estado do Mato Grosso do Sul, da região Centro-Oeste e do Brasil. Foram escolhidas as produções de soja e milho pois são as duas principais modalidades agrícolas do país, seguido pela cana de açucar, que tem mais expressividade no estado de São Paulo e por isso ficou de fora das análises.')
    st.write('O Agro brasileiro, que vem de sua maior parte da região Centro-Oeste do Brasil, sendo aproximadamente 50% da produção de soja so país advinda do estado do Mato Grosso, alimenta o mundo todo. Nossa produção garante a segurança alimentar mundial e equivale a cerca de 25% do PIB brasileiro. Quando alguém falar em TV aberta, em horário nobre, em um dos programas mais assistidos do país que o Agro é fascista, não se deixe levar: é MENTIRA!')
    st.write('Agro é tech! Agro é pop! Agro é tudo!')

    st.subheader('Produção de soja')
    agro_col1, agro_spc, agro_col2 = st.columns([3, 1, 3])

    soja_ms_co_perc = round((soja_ms / soja_co) * 100, 2)
    soja_ms_brasil_perc = round((soja_ms / soja_brasil) * 100, 2)
    
    with agro_col1:
        st.subheader('MS vs Centro Oeste')
        st.pyplot(figSojaMSCO)
        st.write('Produção de soja no MS: ', f(soja_ms), 'toneladas')
        st.write('Produção de soja no Centro-Oeste: ', f(soja_co), 'toneladas')
        st.write('Representa ', str(soja_ms_co_perc), '% da produção de soja no Centro-Oeste')

    with agro_col2:
        st.subheader('MS vs Brasil')
        st.pyplot(figSojaMSBR)
        st.write('Produção de soja no MS: ', f(soja_ms), 'toneladas')
        st.write('Produção de soja no Brasil: ', f(soja_brasil), 'toneladas')
        st.write('Representa ', str(soja_ms_brasil_perc), '% da produção de soja no Brasil')

    agro_col1, agro_spc, agro_col2 = st.columns([3, 1, 3])
    
    with agro_col1:
        st.subheader('MS vs MT vs GO')
        st.pyplot(figSojaMSMTGO);
        st.write('Produção de soja no MS: ', f(soja_ms), 'toneladas')
        st.write('Produção de soja no MT: ', f(soja_mt), 'toneladas')
        st.write('Produção de soja no GO: ', f(soja_go), 'toneladas')


    st.subheader('Produção de milho')
    agro_col1, agro_spc, agro_col2 = st.columns([3, 1, 3])

    milho_ms_co_perc = round((milho_ms / milho_co) * 100, 2)
    milho_ms_brasil_perc = round((milho_ms / milho_brasil) * 100, 2)

    with agro_col1:
        st.subheader('MS vs Centro Oeste')
        st.pyplot(figMilhoMSCO)
        st.write('Produção de milho no MS: ', f(milho_ms), ' toneladas')
        st.write('Produção de milho no Centro-Oeste: ', f(milho_co), ' toneladas')
        st.write('Representa ', str(milho_ms_co_perc), '% da produção de milho no Centro-Oeste')

    with agro_col2:
        st.subheader('MS vs Brasil')
        st.pyplot(figMilhoMSBR)
        st.write('Produção de milho no MS: ', f(milho_ms), ' toneladas')
        st.write('Produção de milho no Brasil: ', f(milho_brasil), ' toneladas')
        st.write('Representa ', str(milho_ms_brasil_perc), '% da produção de milho no Brasil')

    agro_col1, agro_spc, agro_col2 = st.columns([3, 1, 3])
    
    with agro_col1:
        st.subheader('MS vs MT vs GO')
        st.pyplot(figMilhoMSMTGO);
        st.write('Produção de milho no MS: ', f(milho_ms), 'toneladas')
        st.write('Produção de milho no MT: ', f(milho_mt), 'toneladas')
        st.write('Produção de milho no GO: ', f(milho_go), 'toneladas')
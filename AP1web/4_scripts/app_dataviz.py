import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Configuração inicial da página
st.set_page_config(page_title="Computadores Pichau", layout="wide")
st.title("🖥️ Computadores Pichau")
st.markdown("Este painel apresenta uma análise dos processadores e armazenamento disponíveis, com gráficos interativos e métricas.")
st.sidebar.header('Selecione o tipo de filtro desejado para seu computador:')
st.sidebar.header("Filtros:")


#conexão banco de dados
conn = sqlite3.connect("AP1web/4_scripts/banco.db")
query = "SELECT * FROM dados;"
dados_gerais = pd.read_sql_query(query, conn)
conn.close()



# Aplicação de filtros
processador_opcao = st.sidebar.selectbox('Selecione o tipo de processador', ['Todos', 'AMD', 'Intel'])
armazenamento = st.sidebar.selectbox("Selecione a quantidade de armazenamento", ["Todos"] + list(dados_gerais["armazenamento"].unique()))
parcelas_opcao = st.sidebar.selectbox("Selecione o número de parcelas", ["Todos"] + list(dados_gerais["valor parcelado"].unique()))

# Filtros aplicados
dados_filtrados = dados_gerais.copy()
if processador_opcao != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['processador'].str.contains(processador_opcao, case=False, na=False)]
if armazenamento != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["armazenamento"] == armazenamento]
if parcelas_opcao != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["valor parcelado"] == parcelas_opcao]

# Exibição de métricas
if not dados_filtrados.empty:
    metrics = dados_filtrados['precos'].describe()
    media = metrics["mean"]
    mediana = metrics["50%"]
    desvio_padrao = metrics["std"]
else:
    media = mediana = desvio_padrao = 0

col1, col2, col3 = st.columns(3)
col1.metric(label="Média Total", value=f"{media:.2f}")
col2.metric(label="Mediana Total", value=f"{mediana:.2f}")
col3.metric(label="Desvio Padrão", value=f"{desvio_padrao:.2f}")

# Expanders e gráficos
expander1 = st.expander('Gráficos Univariados')
expander2 = st.expander('Gráficos Multivariados')

with expander1:
    fig = px.histogram(dados_filtrados, x='processador', title='Quantidade dos processadores')
    fig2 = px.pie(dados_filtrados, names='armazenamento', title='Proporção do armazenamento dos computadores')
    fig3 = px.box(dados_filtrados, y='precos', title='Boxplot dos Preços')
    st.plotly_chart(fig)
    st.write("Análise: Um gráfico que permite ver a quantidade de processadores")
    st.plotly_chart(fig2)
    st.write("Análise: Nos mostra a proporção da quantidade de processadores")
    st.plotly_chart(fig3)
    st.write("Análise: Identifica a variação dos preços dos computadores")

with expander2:
    fig4 = px.bar(dados_filtrados, x='armazenamento', y='precos', title='Armazenamento por Preços')
    fig5 = px.bar(dados_filtrados, x='processador', y='precos', title="Preços por Processador")
    fig6 = px.bar(dados_filtrados, x='precos', y='nome do produto', title="Preços por Computadores")
    st.plotly_chart(fig4)
    st.write("Análise: Um gráfico mostrando o armazenamento por preços")
    st.plotly_chart(fig5)
    st.write("Análise: Nos Permite identificar a variação de preços em relação aos processadores")
    st.plotly_chart(fig6)
    st.write('Análise: Um gráfico que permite ver computadores em relação ao seu preço')

import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!')
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect('Selecione os produtos', sorted(dados['Produto'].unique()), sorted(dados['Produto'].unique()))
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
with st.sidebar.expander('Categoria do Produto'):
    categoria_produto = st.multiselect('Selecione a Categoria', sorted(dados['Categoria do Produto'].unique()), sorted(dados['Categoria do Produto'].unique()))
with st.sidebar.expander('Frete'):
    frete = st.slider('Selecione o valor do Frete', dados['Frete'].min(), dados['Frete'].max(), (dados['Frete'].min(), dados['Frete'].max()))
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o Vendedor', sorted(dados['Vendedor'].unique()),sorted(dados['Vendedor'].unique()))
with st.sidebar.expander('Local da Compra'):
    local_compra = st.multiselect('Selecione a UF',sorted(dados['Local da compra'].unique()), sorted(dados['Local da compra'].unique()))
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a Nota de Avaliação', 1,5,(1,5))
with st.sidebar.expander('Tipo de Pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', sorted(dados['Tipo de pagamento'].unique()), sorted(dados['Tipo de pagamento'].unique()))
with st.sidebar.expander('Quantidade de Parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', dados['Quantidade de parcelas'].min(), dados['Quantidade de parcelas'].max(), (dados['Quantidade de parcelas'].min(),dados['Quantidade de parcelas'].max()))

query = '''
        Produto in @produtos and \
        @preco[0] <= Preço <= @preco[1] and\
        @data_compra[0] <= `Data da Compra` <= @data_compra[1] and\
        `Categoria do Produto` in @categoria_produto and\
        @frete[0] <= Frete <= @frete[1] and\
        Vendedor in @vendedor and\
        `Local da compra` in @local_compra and\
        @avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and\
        `Tipo de pagamento` in @tipo_pagamento and\
        @qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo:')
col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input('',label_visibility='collapsed', value = 'dados')
    nome_arquivo += '.csv'
with col2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)
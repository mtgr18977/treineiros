import streamlit as st
import pandas as pd
from collections import defaultdict
import os

def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        st.error(f"O arquivo '{arquivo}' não foi encontrado no diretório do script.")
        return None
    try:
        return pd.read_csv(arquivo, delimiter=',')
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {str(e)}")
        return None

def analisar_treinadores(df):
    treinadores_stats = defaultdict(lambda: {'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0})
    
    for _, row in df.iterrows():
        tecnico_mandante = row['tecnico_mandante']
        tecnico_visitante = row['tecnico_visitante']
        vencedor = row['vencedor']
        
        treinadores_stats[tecnico_mandante]['jogos'] += 1
        treinadores_stats[tecnico_visitante]['jogos'] += 1
        
        if vencedor == row['mandante']:
            treinadores_stats[tecnico_mandante]['vitorias'] += 1
            treinadores_stats[tecnico_visitante]['derrotas'] += 1
        elif vencedor == row['visitante']:
            treinadores_stats[tecnico_visitante]['vitorias'] += 1
            treinadores_stats[tecnico_mandante]['derrotas'] += 1
        else:
            treinadores_stats[tecnico_mandante]['empates'] += 1
            treinadores_stats[tecnico_visitante]['empates'] += 1
    
    return treinadores_stats

def analisar_formacoes(df):
    formacoes_mandante = df['formacao_mandante'].value_counts()
    formacoes_visitante = df['formacao_visitante'].value_counts()
    return formacoes_mandante, formacoes_visitante

st.set_page_config(page_title="Dashboard de Treinadores e Formações", layout="wide")
st.title("Análise de Treinadores e Formações do Campeonato Brasileiro")

arquivo_csv = "campeonato-brasileiro-full.csv"
df = carregar_dados(arquivo_csv)

if df is not None:
    treinadores_stats = analisar_treinadores(df)
    formacoes_mandante, formacoes_visitante = analisar_formacoes(df)

    st.header("Análise de Treinadores")
    treinador_selecionado = st.selectbox("Selecione um treinador:", list(treinadores_stats.keys()))
    
    if treinador_selecionado:
        stats = treinadores_stats[treinador_selecionado]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Jogos", stats['jogos'])
        col2.metric("Vitórias", stats['vitorias'])
        col3.metric("Empates", stats['empates'])
        col4.metric("Derrotas", stats['derrotas'])

        aproveitamento = (stats['vitorias'] * 3 + stats['empates']) / (stats['jogos'] * 3) * 100
        st.metric("Aproveitamento", f"{aproveitamento:.2f}%")

    st.header("Análise de Formações")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Formações Mandante")
        st.bar_chart(formacoes_mandante.head(5))

    with col2:
        st.subheader("Top 5 Formações Visitante")
        st.bar_chart(formacoes_visitante.head(5))

    st.header("Comparação de Formações")
    formacoes_df = pd.DataFrame({
        'Mandante': formacoes_mandante,
        'Visitante': formacoes_visitante
    }).fillna(0)

    st.bar_chart(formacoes_df)

else:
    st.error("Não foi possível carregar os dados. Por favor, verifique o arquivo CSV.")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard de Clubes', page_icon='⚽', layout='wide')

st.title('⚽ Dashboard de Clubes')
st.caption('Análise da Tabela de Clubes — 2008 a 2017')

try:
    df = pd.read_csv('Tabela_Clubes.csv')
except FileNotFoundError:
    st.error('Coloque o arquivo Tabela_Clubes.csv na mesma pasta deste app.py.')
    st.stop()

# Tratamento dos dados
df['Idade_Media'] = pd.to_numeric(df['Idade_Media'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
df[['Gols_Feitos', 'Gols_Sofridos']] = df['GolsF/S'].astype(str).str.split(':', expand=True)
df['Gols_Feitos'] = pd.to_numeric(df['Gols_Feitos'], errors='coerce')
df['Gols_Sofridos'] = pd.to_numeric(df['Gols_Sofridos'], errors='coerce')

# Sidebar
st.sidebar.header('🔎 Filtros')
anos = sorted(df['Ano'].dropna().unique().tolist(), reverse=True)
ano = st.sidebar.selectbox('Ano', ['Todos'] + anos)

clubes_disponiveis = sorted(df['Clubes'].dropna().unique().tolist())
clubes = st.sidebar.multiselect('Clubes', clubes_disponiveis)

dados = df.copy()
if ano != 'Todos':
    dados = dados[dados['Ano'] == ano]
if clubes:
    dados = dados[dados['Clubes'].isin(clubes)]

# Indicadores
c1, c2, c3, c4 = st.columns(4)
c1.metric('🏟️ Clubes', dados['Clubes'].nunique())
c2.metric('✅ Vitórias', int(dados['Vitorias'].sum()))
c3.metric('⚽ Gols feitos', int(dados['Gols_Feitos'].sum()))
c4.metric('💰 Valor total', f"R$ {dados['Valor_total'].sum()/1_000_000:.1f} mi")

st.divider()

# Gráfico 1
st.subheader('🏆 Ranking por vitórias')
vitorias = (dados.groupby('Clubes', as_index=False)['Vitorias'].sum()
            .sort_values('Vitorias', ascending=False).head(10))
fig1 = px.bar(vitorias, x='Clubes', y='Vitorias', title='Top 10 clubes por número de vitórias')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2
st.subheader('⚽ Saldo de gols')
saldo = (dados.groupby('Clubes', as_index=False)['Saldo'].sum()
         .sort_values('Saldo', ascending=False).head(10))
fig2 = px.bar(saldo, x='Clubes', y='Saldo', title='Top 10 clubes por saldo de gols')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3
st.subheader('💰 Valor dos elencos')
valores = (dados.groupby('Clubes', as_index=False)['Valor_total'].sum()
           .sort_values('Valor_total', ascending=False).head(10))
fig3 = px.bar(valores, x='Clubes', y='Valor_total', title='Top 10 clubes por valor total')
st.plotly_chart(fig3, use_container_width=True)

# Evolução por ano
st.subheader('📈 Evolução das vitórias por ano')
serie = dados.groupby('Ano', as_index=False)['Vitorias'].sum().sort_values('Ano')
fig4 = px.line(serie, x='Ano', y='Vitorias', markers=True, title='Total de vitórias por ano')
st.plotly_chart(fig4, use_container_width=True)

# Tabela
st.subheader('📊 Dados')
st.dataframe(dados, use_container_width=True, hide_index=True)

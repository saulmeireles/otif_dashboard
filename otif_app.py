import pandas as pd
import streamlit as st
import time as ts
from datetime import time
import json

# Visualização de dados
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import matplotlib.pyplot as plt
# import numpy as np
import locale

# Configurando a formatação para o padrão brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Configuração de layout da página:
st.set_page_config(layout="wide")

# ------- load data
# carregando os dados:
df = pd.read_csv('D:/Documentos/Projetos_vs_code/dashboard_python/otif.csv')

# ------- modelagem

# pegando a quantidade de pedidos
df['qtd'] = 1

# Mapeamento de estados para regiões
estado_regiao = {
    'Acre': 'Norte', 'Alagoas': 'Nordeste', 'Amapá': 'Norte', 'Amazonas': 'Norte', 'Bahia': 'Nordeste', 'Ceará': 'Nordeste', 'Distrito Federal': 'Centro-Oeste',
    'Espírito Santo': 'Sudeste', 'Goiás': 'Centro-Oeste', 'Maranhão': 'Nordeste', 'Mato Grosso': 'Centro-Oeste', 'Mato Grosso do Sul': 'Centro-Oeste', 'Minas Gerais': 'Sudeste',
    'Pará': 'Norte', 'Paraíba': 'Nordeste', 'Paraná': 'Sul', 'Pernambuco': 'Nordeste', 'Piauí': 'Nordeste', 'Rio de Janeiro': 'Sudeste', 'Rio Grande do Norte': 'Nordeste',
    'Rio Grande do Sul': 'Sul', 'Roraima': 'Norte', 'Rondônia': 'Norte', 'Santa Catarina': 'Sul', 'São Paulo': 'Sudeste', 'Sergipe': 'Nordeste', 'Tocantins': 'Norte'
}

# Adicionando a coluna de região ao dataframe
df['Regiao'] = df['Estado'].map(estado_regiao)

# Verificação de valores NaN após o mapeamento
if df['Regiao'].isna().any():
    st.warning('Alguns estados não foram mapeados corretamente para suas regiões. Verifique a coluna "Estado" no seu dataframe.')

# Extraindo o mês da Data de Expedição
df['Mes'] = pd.to_datetime(df['Data Expedição']).dt.strftime('%B').str.capitalize()
# Criando um dicionário para mapear os nomes dos meses para números
mes_ordenacao = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
# Adicionando uma coluna para os números dos meses
df['Mes_num'] = df['Mes'].map(mes_ordenacao)

# ------- Filtro e sidebar
with st.sidebar:
    st.title('🚚 S/A Logística')
    st.subheader('Filtros')

    selected_transportador = st.multiselect('Selecione o transportador', sorted(df['Nome Transportador'].unique()))
    selected_estados = st.multiselect('Selecione o Estado', sorted(df['Estado'].unique()))
    selected_mes = st.multiselect('Selecione o Mês', sorted(df['Mes'].unique(), key=lambda x: mes_ordenacao[x]))
    selected_regiao = st.multiselect('Selecione a Região', sorted(df['Regiao'].dropna().unique()))

# Filtrando o dataframe com base nas seleções
df_filtered = df
if selected_transportador:
    df_filtered = df_filtered[df_filtered['Nome Transportador'].isin(selected_transportador)]
if selected_estados:
    df_filtered = df_filtered[df_filtered['Estado'].isin(selected_estados)]
if selected_mes:
    df_filtered = df_filtered[df_filtered['Mes'].isin(selected_mes)]
if selected_regiao:
    df_filtered = df_filtered[df_filtered['Regiao'].isin(selected_regiao)]

# ------- cálculo de métricas

# Status de entrega:
# Filtrando as categorias 
entrega_sem_ocorrencia = df_filtered[df_filtered['Ocorrência de Entrega'] == 'Sem Ocorrência']
entrega_com_avaria = df_filtered[df_filtered['Ocorrência de Entrega'] == 'Entrega com Avaria']

# Contando pedidos para cada categoria:
qtd_sem_ocorrencia = entrega_sem_ocorrencia.shape[0]
qtd_com_avaria = entrega_com_avaria.shape[0]

# Calculando os percentuais
total_entregas = df_filtered.shape[0]
entregas_on_time = df_filtered[df_filtered['On Time'] == 'On Time'].shape[0]
entregas_late = df_filtered[df_filtered['On Time'] == 'Late Time'].shape[0]
entregas_in_full = df_filtered[df_filtered['In Full'] == 'In Full'].shape[0]

percentual_on_time = (entregas_on_time / total_entregas) * 100
percentual_late = (entregas_late / total_entregas) * 100
percentual_in_full = (entregas_in_full / total_entregas) * 100

# Calculando o total de faturamento
total_faturamento = df_filtered['Valor Nota Fiscal'].sum()
# Formatando o total de faturamento em Real (moeda)
total_faturamento_formatado = locale.currency(total_faturamento, grouping=True)

# Agrupando o número de pedidos por região
pedidos_por_regiao = df_filtered['Codigo_IBGE'].value_counts().reset_index()
pedidos_por_regiao.columns = ['Codigo_IBGE', 'qtd']

# ------ Funções para gráficos

# Função para criar gráficos de rosca
def grafico_rosca(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color =['#29b5e8', '#155F7A']   
    elif input_color == 'green':
        chart_color = ['#27AE60', '#12783D']    
    elif input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']    

    fig = go.Figure(data=[go.Pie(
        values=[100-input_response, input_response], 
        hole=.7,
        marker=dict(colors=[chart_color[1], chart_color[0]]),
        textinfo='none'  # Desativa os rótulos laterais
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(t=40, b=0, l=0, r=0),
        annotations=[dict(text=f'{input_response:.2f}%', x=0.5, y=0.5, font_size=20, showarrow=False, font=dict(color=chart_color[0]))],
        width=180,
        height=180,
        title={
            'text': input_text,
            'y': 0.98,  # Posição do título em relação ao gráfico
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    return fig


# Carregando o arquivo json com as coordenadas das regiões
with open('D:/Documentos/Projetos_vs_code/dashboard_python/uf.json', 'r') as f:
    arquivo_json = json.load(f)

  
# Função do gráfico de Mapa Coropletico
def mapa_coropletico(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, 
                               geojson=arquivo_json,
                               locations=input_id, 
                               featureidkey='properties.GEOCODIGO',
                               color=input_column,
                               color_continuous_scale=input_color_theme,
                               labels={input_column: 'Pedidos'}
                               #title='Pedidos por Estado'
                              )
    
    choropleth.update_geos(
        fitbounds='locations',
        visible=False,
        lonaxis_range=[-75, -33],
        lataxis_range=[-34, 6]
    )
    
    choropleth.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo do gráfico transparente
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Fundo do papel transparente
        geo=dict(
            bgcolor='rgba(0, 0, 0, 0)'  # Fundo do mapa transparente
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=550  # Ajuste a altura do gráfico conforme necessário
    )
    
    return choropleth

# Função para criar gráfico de barras 
def grafico_barras(df):
    df['Mes'] = pd.to_datetime(df['Data Expedição']).dt.strftime('%Y-%m')
    df_grouped = df.groupby(['Mes', 'On Time']).size().reset_index(name='Count')
    
    # Criando uma lista de todos os meses do ano
    all_months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M').strftime('%Y-%m').tolist()
    df_grouped['Mes'] = pd.Categorical(df_grouped['Mes'], categories=all_months, ordered=True)
    df_grouped = df_grouped.sort_values('Mes')

    # Definindo as cores para "On Time" e "Late Time"
    colors = {'On Time': '#29b5e8', 'Late Time': '#E74C3C'}

    # Configurando a ordem das categorias para garantir que 'On Time' fique na frente de 'Late Time'
    df_grouped['On Time'] = pd.Categorical(df_grouped['On Time'], categories=['On Time', 'Late Time'], ordered=True)

    
    bar_chart = px.bar(df_grouped, x='Mes', y='Count', color='On Time',
                       color_discrete_map=colors,
                       labels={'Mes': 'Mês', 'Count': 'Número de Pedidos', 'On Time': 'Status'},
                       title='Pedidos On Time e Late por Mês',
                       barmode='group',
                       text='Count')  # Orientação vertical é padrão

    bar_chart.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=40, b=0, l=0, r=0),
        height=250  # Ajuste a altura do gráfico conforme necessário
    )

    # bar_chart.update_xaxes(tickmode='array', tickvals=all_months, ticktext=all_months, tickangle=-45)
    bar_chart.update_traces(textfont_color='white')  # Define a cor dos rótulos dos dados para branco

    
    return bar_chart


# Função para criar um gráfico de barras empilhadas
def barras_empillhadas(df):
    # Agrupar dados por fornecedor e status de entrega
    supplier_status_data = df.groupby(['Nome Transportador', 'On Time']).size().unstack(fill_value=0)
    
    # Calcular as porcentagens
    supplier_status_data['Total'] = supplier_status_data['Late Time'] + supplier_status_data['On Time']
    supplier_status_data['On Time %'] = (supplier_status_data['On Time'] / supplier_status_data['Total']) * 100
    supplier_status_data['Late Time %'] = (supplier_status_data['Late Time'] / supplier_status_data['Total']) * 100
    
    # Ordenar por maior percentual de On Time
    supplier_status_data = supplier_status_data.sort_values(by='On Time %', ascending=True)
    
    # Criar o gráfico de barras empilhadas com fornecedores no eixo y
    stacked_bar_chart = go.Figure(data=[
        go.Bar(
            name='On Time', 
            y=supplier_status_data.index, 
            x=supplier_status_data['On Time %'], 
            orientation='h', 
            marker_color='#29b5e8',
            text=supplier_status_data['On Time %'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            insidetextanchor='middle'
        ),
        go.Bar(
            name='Late Time', 
            y=supplier_status_data.index, 
            x=supplier_status_data['Late Time %'], 
            orientation='h', 
            marker_color='#E74C3C',
            text=supplier_status_data['Late Time %'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            insidetextanchor='middle'
        )
    ])
    
    # Atualizar o layout do gráfico
    stacked_bar_chart.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=40, b=0, l=0, r=0),
        height=600,
        title='Entregas % On Time/Late Time por Fornecedor',
        xaxis=dict(title='Percentual de Entregas (%)'),
        yaxis=dict()
    )

   
    stacked_bar_chart.update_traces(textfont_color='white')  # Define a cor dos rótulos dos dados para branco

    
    return stacked_bar_chart


#------- Criação do Dahsboard

# Grade para o dashboard
col = st.columns((1.5, 3.8, 1.8), gap='small')
# Primeira coluna
with col[0]:
    # Formatação do total de pedidos com separador de milhar
    total_entregas_formatado = locale.format_string("%d", total_entregas, grouping=True)

    # Mostrar a quantidade total de pedidos com separadores de milhar
    st.metric("Total de Pedidos", total_entregas_formatado)
    
    # Mostrar o total de faturamento formatado em Real (moeda)
    st.metric("Total de Faturamento", total_faturamento_formatado)

    st.markdown('#### Desempenho de Entrega')
    st.plotly_chart(grafico_rosca(percentual_on_time, 'On Time', 'blue'), use_container_width=False)
    # Gráfico de rosca para o percentual de late time
    st.plotly_chart(grafico_rosca(percentual_late, 'Late Time', 'red'), use_container_width=False)
    # Gráfico de rosca para o percentual de in full
    st.plotly_chart(grafico_rosca(percentual_in_full, 'In Full', 'green'), use_container_width=False)

# Segunda coluna
with col[1]:
    st.subheader('Pedidos por Estado')
    fig_mapa = mapa_coropletico(pedidos_por_regiao, 'Codigo_IBGE', 'qtd', 'Blues')
    st.plotly_chart(fig_mapa, use_container_width=True)

    fig_bar_chart = grafico_barras(df_filtered)
    st.plotly_chart(fig_bar_chart, use_container_width=True)

# Terceira coluna
with col[2]:
    st.plotly_chart(barras_empillhadas(df_filtered), use_container_width=True)
    st.write('''
            - :orange[**Dados**]: Dados fictícios criados com a biblioteca Faker
            - :blue[**On Time / Late Time**]: Pedido entregues dentro e fora do prazo de entrega
            - :blue[**In Full**]: Pedidos que foram entregues dentro do prazo e sem nenhuma avaria ou problema na entrega
            - :orange[**Linkedin**]: https://www.linkedin.com/in/saulmeireles/
            ''')

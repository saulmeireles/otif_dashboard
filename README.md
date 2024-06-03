# Dashboard de Logística

Este projeto é um dashboard interativo para visualização e análise de dados de entregas logísticas, criado utilizando Python, Streamlit e Plotly. O dashboard permite filtrar e visualizar dados com base em diversos critérios, como transportadores, estados, meses e regiões do Brasil.

## Funcionalidades

- **Visualização de Dados**: Gráficos interativos de rosquinha, barras verticais, barras horizontais e mapas coropléticos.
- **Filtros Dinâmicos**: Filtragem de dados por transportador, estado, mês e região.
- **Indicadores Chave**: Exibição de métricas de desempenho de entrega, como percentuais de entregas no prazo (On Time), entregas atrasadas (Late Time) e entregas completas (In Full).
- **Informações Financeiras**: Cálculo e formatação do total de faturamento das entregas.

## Requisitos

- Python 3.8 ou superior
- Pacotes Python:
  - pandas
  - streamlit
  - seaborn
  - plotly
  - matplotlib
  - numpy
  - locale

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Certifique-se de que o locale está configurado corretamente. No Windows, pode ser necessário definir o locale manualmente:
    ```python
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    ```

## Uso

1. Execute o aplicativo Streamlit:
    ```sh
    streamlit run otif_app.py
    ```

2. Abra o navegador e acesse `http://localhost:8501` para visualizar o dashboard.

## Estrutura do Projeto

- `otif_app.py`: Arquivo principal do aplicativo Streamlit.
- `otif.csv`: Arquivo CSV contendo os dados de entrega.
- `uf.json`: Arquivo JSON com as coordenadas das regiões do Brasil.
- `requirements.txt`: Arquivo de requisitos com as dependências do projeto.


## Contato

- [LinkedIn](https://www.linkedin.com/in/saulmeireles/)

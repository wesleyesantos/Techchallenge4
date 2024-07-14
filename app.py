import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise do Preço do Petróleo Brent",layout="wide", page_icon="https://github.com/wesleyesantos/Techchallenge4/raw/main/ico.ico", initial_sidebar_state="expanded")
st.sidebar.image('https://github.com/wesleyesantos/Techchallenge4/blob/main/fiap_alura.png?raw=true')
with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options=[ 'Página Inicial','Análise dos dados','Dashboard',
        'Bibliografia'],
        icons=['house', 'activity', 'kanban', 'book'],
        menu_icon = "cast",
        default_index = 1,
        )
st.sidebar.markdown("___")


if selected == 'Página Inicial':
    st.title(":orange[Análise do cenário do combústivel no Brasil]")
    st.header(":orange[Cenário do Combustível]")
    st.markdown("Desenvolvedor: Wesley Estevão dos Santos")
    st.markdown("""
Fonte: <a href="http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view" target="_blank">🌎 IPEA </a>
""", unsafe_allow_html=True) 
    st.subheader(    ":orange[Resumo da Análise]",divider="orange",)
    st.markdown(
    """
        Para essa análise realizei o ETL inicialmente pelo excel para realizar os ajustes iniciais de formatação da base, depois segui para o python onde iniciei a análise exploratória dos dados, 
        análises de estatística básica, identificar os pontos marcantes da base de dados disponibilizada, incluir bases adicionais, fazer todos os links com as bases externas, 
        testar melhores visualizações e começar a separar a base para trabalhar na predição.
    """)

    st.subheader(":orange[Objetivo]", divider="orange")
    st.markdown(
        """
        - Analisar o histórico de preços do petróleo Brent e criar modelos de machine learning que auxiliem na previsão do seu preço futuro; 
        - Criar insights quanto a maiores flutuações dos valores do combustível; 
        - Realizar calculo do MVP do combustível;
        - Criar um plano para fazer deploy do modelo em produção 
    """)

    st.subheader(":orange[Metodologia]", divider="orange")
    st.markdown(
        """
        - Dados foram disponibilizados pelo site da ipeadata.gov.br
        - Com base na análise feita, são criados 2 modelos distintos que tem o intuito de prever o preço futuro do barril de petróleo.
        - A respeito do modelo criado, o  modelo utiliza a biblioteca Prophet da Meta""")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif selected == 'Análise dos dados':
    st.header(":orange[Análise dos dados]")
    
    st.subheader(":orange[Iniciando o ETL dos dados]", divider="orange")
    st.markdown('''
                - Os dados foram trabalhados inicialmente no excel, para questões de ajustes dos valores e datas, após ajuste incial foi feito upload da base no github de onde utilizei esse link para subir essas informações no python e iniciar toda a análise exploratória dos dados.
                - No Excel cheguei utilizar funções básicas como direito, esquerdo, concatenar, etc, para deixar os dados o mais próximo do que precisava sem muita necessidade de ajustes no python.
                ''')
    
    st.subheader(":orange[Análise Exploratória]", divider="orange")
    st.markdown('''Após primeira etapa fiz upload dos dados no python utilizando o pandas.''')
    
    code= '''
            Import pandas as pd
            df = pd.read_csv('https://github.com/wesleyesantos/Techchallenge4/raw/main/preco_combustivel.csv',sep=';')'''
    st.code(code)
    
    st.markdown('''
                Dei um df.head() pra visualizar as primeiras linhas do meu dataframe, e após fazer o df.info(), observei que nos tipos de dados a data subiu como string, mesmo ajustando no excel o python não reconheceu as datas, tentei usar o parse dates, mas mesmo assim não foi possível tive que ajustar o tipo dos dados. Como trabalhei com o Google colab a biblioteca datetime é nativa então não precisei instalar nem mesmo importa-la.
                ''')
    code2 = '''
            df['data'] = pd.to_datetime(df['data'])
          '''
    st.code(code2)

    st.markdown('''Fiz describe para analisar maior, menor valor, e valores médios que constavam dentro da base. Na sequência analisei se constavam valores zerados, e realizei o dropna por desencargo para não impactar quando fosse criar meu modelo Prophet.''')
    code3 = '''
            df['preco_barril_usd'].describe()

            df.isnull().sum()

            df = df.dropna(subset=['preco_barril_usd'])
          '''
    st.code(code3)

    st.subheader(":orange[Análise prescritiva]", divider="orange")
    st.markdown('''Plotei um gráfico geral para puxar maiores picos de valores dentre os anos e começar a gerar os insights e poder aproveitar esses insights para ajustar os outliers no meu modelo mais pra frente e já poder criar meu storytelling quanto a acontecimentos dentre os anos.''')
    df = pd.read_csv('https://github.com/wesleyesantos/Techchallenge4/raw/main/preco_combustivel.csv',sep=';')  
    df['data'] = pd.to_datetime(df['data'])
    fig_date = px.bar(df, x= 'data', y='preco_barril_usd', title= 'Valor Petróleo Brent por dia(USD)', labels={'data': 'Data', 'preco_barril_usd': 'Preço'}, width=1200, height=500)
    st.plotly_chart(fig_date)

    st.markdown('''##### Analisando o gráfico identifiquei alguns dos maiores picos que foram nos anos:''')
    st.markdown('''
                - 1990
                - 2000
                - 2008
                - 2011
                - 2022
                     ''')

    st.markdown('''Com isso comecei a trabalhar encima desses anos para criação de insights para criação do storytelling do meu dashboard.''')

 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

elif selected == 'Dashboard':
    with st.sidebar:
        selected = option_menu(
        menu_title = 'Dashboard Menu',options=[ 'Análise Histórica','Modelo de Predição','Conclusão'], 
        icons = ['kanban', 'kanban','kanban', 'house'],
        menu_icon = "cast", default_index = 0,)

    df = pd.read_csv('https://github.com/wesleyesantos/Techchallenge4/raw/main/preco_combustivel.csv',sep=';')  
    df['data'] = pd.to_datetime(df['data'])
    df_impact = df[(df['data'].dt.year == 1990) | (df['data'].dt.year == 2000) | (df['data'].dt.year == 2008) | (df['data'].dt.year == 2011) | (df['data'].dt.year == 2022)]
    df_impact['year'] = df_impact['data'].dt.year
    df_impact = pd.DataFrame(df_impact.groupby('year')['preco_barril_usd'].mean()).reset_index()
    df_impact['preco_barril_usd'] = df_impact['preco_barril_usd'].round(2)

    if selected == 'Análise Histórica':
        st.title(":orange[Análise Histórica]")
        
        start_date, end_date = st.slider(
        "Selecione o intervalo de datas",
        min_value=df['data'].min().to_pydatetime(),
        max_value=df['data'].max().to_pydatetime(),
        value=(df['data'].min().to_pydatetime(), df['data'].max().to_pydatetime()),
        format="YYYY-MM-DD")  
        filtered_df = df[(df['data'] >= pd.to_datetime(start_date)) & (df['data'] <= pd.to_datetime(end_date))]

        #colunas para os gráficos 
        col_grap, col_grap2 = st.columns([3,1.5])
                
        #Gráfico 1
        fig_date = px.bar(filtered_df, x= 'data', y='preco_barril_usd', title= 'Valor Petróleo Brent por dia(USD)', labels={'data': 'Data', 'preco_barril_usd': 'Preço'}, width=900, height=500)
        with col_grap:
            st.plotly_chart(fig_date, use_container_width=True)

        #Gráfico 2
        fig_impact = px.pie(df_impact, names='year', values='preco_barril_usd', title='Preço do combustível em dólar por ano',labels={'data': 'Data', 'preco_barril_usd': 'Preço'}, width=500, height=500)
        with col_grap2:
            st.plotly_chart(fig_impact, use_container_width=True)

 

        st.subheader(":orange[1990]",divider="orange",)
        df_1990 = df[df['data'].dt.year == 1990]
        max_1990 = df_1990['preco_barril_usd'].max()
        min_1990 = df_1990['preco_barril_usd'].min()
        mean_1990 = df_1990['preco_barril_usd'].mean()
        col1, col2, col3 ,col4= st.columns(4)
        with col1: st.metric(label="Maior Valor", value=max_1990)
        with col2: st.metric(label="Menor Valor", value=min_1990)
        with col3: st.metric(label="Valor médio", value= round(mean_1990, 2))
        st.markdown('##### Em 1990, o preço do petróleo Brent foi influenciado por vários fatores. Vou destacar alguns deles:')
        st.markdown('''
        - Crise do Golfo Pérsico: A Invasão do Kuwait pelo Iraque em 1990 levou a uma crise no Golfo Pérsico. Isso resultou em restrições na produção e exportação de petróleo, afetando os preços do Brent.
        - Sanções internacionais: A ONU impôs sanções ao Iraque após a invasão do Kuwait. Isso afetou o fornecimento global de petróleo e contribuiu para a volatilidade dos preços.
        - Recessão econômica: A recessão global no início dos anos 90 também impactou a demanda por petróleo. A menor atividade econômica afetou os preços do Brent.
        ''')

        st.subheader(":orange[2000]",divider="orange",)
        df_2000 = df[df['data'].dt.year == 2000]
        max_2000 = df_2000['preco_barril_usd'].max()
        min_2000 = df_2000['preco_barril_usd'].min()
        mean_2000 = df_2000['preco_barril_usd'].mean()
        col1, col2, col3 ,col4= st.columns(4)
        with col1: st.metric(label="Maior Valor", value=max_2000)
        with col2: st.metric(label="Menor Valor", value=min_2000)
        with col3: st.metric(label="Valor médio", value= round(mean_2000, 2))
        st.markdown('##### Impactos do aumento do combustível no Brasil em 2000 foram significativos e afetaram diversos aspectos da economia. Vamos explorar alguns desses impactos:')
        st.markdown('''
       - Inflação:
            - O aumento nos preços dos combustíveis contribuiu para a inflação no país. A cada 1% de aumento no preço do combustível, há mais de 0,04 ponto percentual de impacto no Índice Nacional de Preços ao Consumidor Amplo (IPCA). Por exemplo, se o IPCA sobe 2%, cerca de 0,08 ponto percentual é devido ao aumento do combustível.
            - Muitos produtos e mercadorias são transportados por caminhões, e o aumento no custo do combustível se traduz em custos de transporte mais altos. Isso, por sua vez, pode levar a um aumento nos preços de bens e serviços, alimentando a inflação.
        - Produção e Consumo de Petróleo:
            -  Em 2000, o Brasil produzia e consumia cerca de 40% a mais de petróleo do que consumia anteriormente. No entanto, a capacidade brasileira de transformar petróleo em derivados avançou apenas 4,5%, cobrindo cerca de dois terços do que é produzido, o que representa algo em torno de três milhões de barris diários.''')
  
        st.subheader(":orange[2008]",divider="orange",)
        df_2008 = df[df['data'].dt.year == 2008]
        max_2008 = df_2008['preco_barril_usd'].max()
        min_2008 = df_2008['preco_barril_usd'].min()
        mean_2008 = df_2008['preco_barril_usd'].mean()
        col1, col2, col3 ,col4= st.columns(4)
        with col1: st.metric(label="Maior Valor", value=max_2008)
        with col2: st.metric(label="Menor Valor", value=min_2008)
        with col3: st.metric(label="Valor médio", value= round(mean_2008, 2))

        st.markdown('##### Em 2008, o mercado de petróleo viveu um drama em dois atos. Vamos analisar os principais fatores que influenciaram o preço do petróleo Brent durante esse período:')
        st.markdown('''
        - Crise financeira e Grande Recessão: A crise financeira de 2008 e a subsequente recessão global tiveram um impacto significativo no mercado de petróleo e gás. Os preços do barril de petróleo bruto, que haviam atingido quase USD 150, despencaram para cerca de USD 35 em apenas alguns meses.
        - Queda geral nos preços dos ativos: A recessão levou a uma queda generalizada nos preços dos ativos em todo o mundo. O crédito se contraiu, e as projeções de lucros caíram, afetando também o preço do petróleo.
        - Volatilidade sem precedentes: O preço do petróleo Brent ultrapassou a barreira dos 100 dólares o barril, chegando a 147,50 dólares, antes de sofrer uma queda brusca e meteórica. Essa volatilidade pode ter originado graves problemas de abastecimento.
        ''')
        st.subheader(":orange[2011]",divider="orange",)
        df_2011 = df[df['data'].dt.year == 2011]
        max_2011 = df_2011['preco_barril_usd'].max()
        min_2011 = df_2011['preco_barril_usd'].min()
        mean_2011 = df_2011['preco_barril_usd'].mean()
        col1, col2, col3 ,col4= st.columns(4)
        with col1: st.metric(label="Maior Valor", value=max_2011)
        with col2: st.metric(label="Menor Valor", value=min_2011)
        with col3: st.metric(label="Valor médio", value= round(mean_2011, 2))

        st.markdown('##### Em 2011, o preço do petróleo Brent foi influenciado por vários fatores. Vou destacar alguns deles:')
        st.markdown('''
        - Conflitos geopolíticos: A instabilidade política no Oriente Médio e Norte da África afetou a oferta global de petróleo. Conflitos, como a Primavera Árabe, tiveram impacto direto nos preços do Brent.
        - Produção da OPEP: A Organização dos Países Exportadores de Petróleo (OPEP) ajusta sua produção para equilibrar oferta e demanda. Decisões da OPEP em relação à produção afetaram os preços do Brent em 2011.
        - Níveis de estoques: Os níveis globais de estoques de petróleo também influenciam os preços. Estoques baixos indicam maior escassez e preços mais altos.
        - Atividade especulativa: Investidores que compram e vendem contratos futuros podem impactar os preços do Brent, buscando lucrar com flutuações.
        ''')


        st.subheader(":orange[2022]",divider="orange",)
        df_2022 = df[df['data'].dt.year == 2022]
        max_2022 = df_2022['preco_barril_usd'].max()
        min_2022 = df_2022['preco_barril_usd'].min()
        mean_2022 = df_2022['preco_barril_usd'].mean()
        col1, col2, col3 ,col4= st.columns(4)
        with col1: st.metric(label="Maior Valor", value=max_2022)
        with col2: st.metric(label="Menor Valor", value=min_2022)
        with col3: st.metric(label="Valor médio", value= round(mean_2022, 2))
        st.markdown('##### Em 2022, o preço do petróleo Brent foi influenciado por vários fatores. Vou destacar alguns deles:')
        st.markdown('''
    - Recuperação econômica pós-pandemia: Com a retomada das atividades econômicas após a pandemia da Covid-19, houve aumento na demanda por petróleo, impulsionando os preços.
    - Restrições de oferta: Algumas regiões produtoras enfrentaram desafios na produção e exportação de petróleo, o que afetou a oferta global. Isso incluiu eventos como conflitos geopolíticos e interrupções na produção.
    - Previsões otimistas: Analistas de mercado projetaram preços mais altos para o petróleo Brent em 2022. O Goldman Sachs, por exemplo, estimou que o barril atingiria USD 100 no terceiro trimestre. Já o JPMorgan previu que poderia chegar a USD 185 ao final do ano, considerando cenários de fornecimento russo.
        ''')

    elif selected == 'Modelo de Predição':
        st.title(":orange[Modelo de Machine Learn - Prophet]")
        st.subheader(":orange[Código - Prophet]",divider="orange",)
        code = '''
        
        # Importando bibliotecas necessárias
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from prophet import Prophet
        from prophet.diagnostics import cross_validation, performance_metrics
        from prophet.plot import plot_cross_validation_metric
        from sklearn.preprocessing import MinMaxScaler

        # Carregando a base de dados
        df = pd.read_csv('https://github.com/wesleyesantos/Techchallenge4/raw/main/preco_combustivel.csv', sep=';')
        df['data'] = pd.to_datetime(df['data'])

        # Verificando e tratando valores nulos
        print(df.isnull().sum())
        df = df.dropna(subset=['preco_barril_usd'])

        # Preparando os dados para o Prophet
        df_prophet = df[['data', 'preco_barril_usd']]
        df_prophet.columns = ['ds', 'y']
        df_prophet.sort_values('ds', inplace=True)

        # Utilizando os últimos 10 anos de dados para análise
        df_prophet = df_prophet[df_prophet['ds'] >= df_prophet['ds'].max() - pd.DateOffset(years=10)]

        # Normalização dos dados
        scaler = MinMaxScaler()
        df_prophet['y'] = scaler.fit_transform(df_prophet[['y']])

        # Adicionando regressor para capturar impacto da COVID-19
        df_prophet['covid_impact'] = np.where((df_prophet['ds'] >= '2020-03-01') & (df_prophet['ds'] <= '2022-12-31'), 1, 0)

        # Criação do modelo Prophet
        modelo = prophet.Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        modelo.add_regressor('covid_impact')
        modelo.add_country_holidays(country_name='US')  # Adicionando feriados dos EUA como exemplo
        modelo.fit(df_prophet)

        # Criando datas futuras para previsão de 3 meses
        future = modelo.make_future_dataframe(periods=90)
        future['covid_impact'] = np.where((future['ds'] >= '2020-03-01') & (future['ds'] <= '2022-12-31'), 1, 0)
        forecast = modelo.predict(future)

        # Desnormalizando as previsões
        forecast['yhat'] = scaler.inverse_transform(forecast[['yhat']])

        # Desnormalizando os dados reais para plotar corretamente
        df_prophet['y'] = scaler.inverse_transform(df_prophet[['y']])

        # Plotando as previsões
        fig1 = modelo.plot(forecast)
        plt.scatter(df_prophet['ds'], df_prophet['y'], color='r', label='Dados reais')
        plt.legend()
        plt.show()

        fig2 = modelo.plot_components(forecast)
        plt.show()

        # Avaliação do modelo com validação cruzada
        df_cv = cross_validation(modelo, initial='365 days', period='90 days', horizon='90 days')

        # Calculando MAPE manualmente
        df_cv = df_cv[df_cv['y'] != 0]  # Remover valores reais zero
        df_cv['abs_error'] = np.abs(df_cv['y'] - df_cv['yhat'])
        df_cv['mape'] = df_cv['abs_error'] / df_cv['y']
        mape_mean = df_cv['mape'].mean()

        # Printando as métricas de desempenho
        print('MAE: {}'.format(df_cv['abs_error'].mean()))
        print('RMSE: {}'.format(np.sqrt(np.mean((df_cv['y'] - df_cv['yhat'])**2))))
        print('MAPE: {}'.format(mape_mean))

        # Plot da validação cruzada
        fig3 = plot_cross_validation_metric(df_cv, metric='mape')
        plt.show()
        '''
        st.code(code, language='python')

        st.subheader(":orange[Plotagens do modelo]",divider="orange",)
        st.markdown('### Predição de dados')
        image_path = r"C:\Users\Wesley\Desktop\Postech - Módulo 4\Techchallenge 4\predição.png"
        st.image(image_path, caption='Predição de Preços', use_column_width=True)
        st.markdown('### Componentes')
        image_path = r"C:\Users\Wesley\Desktop\Postech - Módulo 4\Techchallenge 4\componentes.png"
        st.image(image_path, caption='Componentes', use_column_width=True)
        st.markdown('### MAPE')
        image_path = r"C:\Users\Wesley\Desktop\Postech - Módulo 4\Techchallenge 4\mape.png"
        st.image(image_path, caption='MAPE', use_column_width=True)

        st.subheader(":orange[Performances]",divider="orange",)
        st.markdown('''O modelo que criei evolui bastante comecei trabalhando com ele onde me trazia um MAPE de 60%, era bem crítico, sabendo que não dava pra utilizar daquela forma continuei tentando o melhor range de data e configuração do modelo, testei a divisão da base 70/30, mas por fim resolvi manter as divisões das bases de treino e teste por 80/20; para o range de tempo utilizado no modelo foi bem dificil pra mim já trabalhei com forecast de curto prazo mas o histórico que utilizava era bem curto e não era ML mas sim outros métodos, depois de muito tempo percebi que o melhor era aumentar o range de tempo que o modelo ganhava um pouco mais de performance, ajustei o range de tempo, inclui a normalização dos dados e trabalhei no outlier que foi impactado pelo covid, no final esse foi o melhor resultado que consegui alcançar para esse modelo trazendo uma análise diária dos dados.''')
        st.markdown('''
                    - MAE: 0.09532551296665125
                    - RMSE: 0.13660528663292823
                    - MAPE: 0.27412167527225867''')

    elif selected == 'Conclusão':
        st.title(":orange[Conclusão]")

        st.markdown('''### Os anos de 1990, 2000, 2008, 2011 e 2022, destacam como eventos geopolíticos, crises econômicas, demanda global e decisões estratégicas de produção influenciam diretamente os preços do petróleo Brent, tornando-o um mercado altamente volátil e sensível a fatores externos e internos.''')
        st.markdown('''### Para meu modelo de predição mesmo o fazendo tantas vezes para chegar no melhor resultado que poderia chegar a predição dele demonstrou que os preços irão subir e que terão alguns picos de queda.''')
        image_path = r"C:\Users\Wesley\Desktop\Postech - Módulo 4\Techchallenge 4\Minions.gif"
        st.image(image_path,width=1000)



    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
elif selected == 'Bibliografia':
   st.header(":orange[Bibliografia]")

   st.markdown('''
               - http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view

               - Relatório Anual da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis) - Publicações anuais que podem fornecer informações históricas e contextuais sobre o mercado de petróleo. https://www.gov.br/anp/pt-br/
               
               -Boletim Mensal de Energia do MME (Ministério de Minas e Energia) - Boletins mensais com dados históricos e análises do setor energético.https://www.gov.br/mme/pt-br
               
               - Relatório Anual da OPEP (Organização dos Países Exportadores de Petróleo) - Relatórios que podem incluir dados e análises sobre o impacto de crises geopolíticas nos preços do petróleo. https://www.opec.org/opec_web/en/
               
               - Brasil Escola - https://brasilescola.uol.com.br/historiag/guerra-golfo.htm

               - Mundo Educação - https://mundoeducacao.uol.com.br/historiageral/guerra-golfo.htm

                - https://agenciabrasil.ebc.com.br/economia/noticia/2022-04/ipca-preco-do-combustivel-impactou-alta-recorde-da-inflacao-oficial
               
               - https://www.ibp.org.br/observatorio-do-setor/snapshots/impacto-dos-combustiveis-na-inflacao/

               - https://oilprice.com

               ''')
    
    st.sidebar.markdown("# Informações Gerais")
    st.sidebar.markdown('''### Desenvolvedor:<BR> Wesley Estevão dos Santos<br><BR>Turma: 3DTAT<br><br> Formação: POSTECH''', unsafe_allow_html=True)
    st.sidebar.markdown("___")

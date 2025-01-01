import datetime as dt
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_echarts import st_echarts

def run():
    st.title("Estacionalidad de los Futuros del USD")

    ticker = "DX-Y.NYB"

    # Selección de fechas
    start = st.date_input("Fecha de inicio", value=dt.datetime(1978, 1, 1))
    end = st.date_input("Fecha de fin", value=dt.datetime.now())

    if start >= end:
        st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
        return

    # Descargar datos
    with st.spinner("Descargando datos..."):
        df = yf.download(ticker, start=start, end=end, interval="1d")
        data = df
        data.reset_index(inplace=True)
        df_visible = pd.DataFrame()
        df_visible['Date'] = data['Date']
        df_visible['Open'] = data['Open']
        df_visible['High'] = data['High']
        df_visible['Low'] = data['Low']
        df_visible['Close'] = data['Close']

    if df.empty:
        st.error("No se encontraron datos para el rango seleccionado.")
        return
    
    # Calcular métricas adicionales
    df["multiplier"] = df["Close"] / df["Open"]
    df['Date'] = pd.to_datetime(df['Date'])
    df["M-D"] = df['Date'].dt.strftime("%m-%d")
    grouped_df = df.groupby("M-D")["multiplier"].mean().reset_index()
    grouped_df["cumprod"] = grouped_df["multiplier"].cumprod()
    max_cumprod = grouped_df["cumprod"].max()
    min_cumprod = grouped_df["cumprod"].min()
    grouped_df["normalized"] = ((grouped_df["cumprod"] - min_cumprod) / (max_cumprod - min_cumprod)) * 100
    grouped_df['M-D'] = '2000-' + grouped_df['M-D']
    grouped_df['M-D'] = pd.to_datetime(grouped_df['M-D'], format='%Y-%m-%d')

    # Agrupar datos para gráficos de barras
    df_visible['Date'] = pd.to_datetime(df_visible['Date'])
    df_visible['Month-day'] = df_visible['Date'].dt.strftime("%m-%d")
    df_visible['Return'] = df_visible['Close'].pct_change().fillna(0)
    daily_seasonality = df_visible.groupby('Month-day').agg(
        count=('Return', 'count'),
        positive=('Return', lambda x: (x > 0).sum()),
        average_gain_loss=('Return', lambda x: x.mean())
    )

    # ---------------------Crear gráfico de líneas plotly-----------------------

    st.subheader("Gráfico Estacional")
    fig = px.line(
        grouped_df,
        x="M-D",
        y="normalized",
        title="Tendencia Estacional del USD",
        template="simple_white",
    )
    # Personalizar el diseño
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickformat="%B", 
            title="Mes"
        ),
        yaxis=dict(title="Tendencia Normalizada (0-100)")
    )
    # Mostrar el gráfico
    fig.update_traces(connectgaps=True)
    st.plotly_chart(fig)

  #---------------------Gráficos de barras por mes.---------------------

    daily_seasonality['Percentage_Positive'] = (daily_seasonality['positive'] / daily_seasonality['count']) * 100
    daily_seasonality['Percentage_Positive'] = daily_seasonality['Percentage_Positive'].round(2)

    # Selección del gráfico en selectbox
    options = ["Estacionalidad Enero", "Estacionalidad Febrero", "Estacionalidad Marzo","Estacionalidad Abril","Estacionalidad Mayo", "Estacionalidad Junio", "Estacionalidad Julio", "Estacionalidad Agosto","Estacionalidad Septiembre", "Estacionalidad Octubre", "Estacionalidad Noviembre", "Estacionalidad Diciembre"]
    selected_chart = st.selectbox("Selecciona el gráfico a mostrar:", options)

    # Mostrar el gráfico seleccionado
    if selected_chart == "Gráfico Estacional":
        fig = px.line(
            grouped_df,
            x="M-D",
            y="normalized",
            title="Tendencia Estacional del USD",
            template="simple_white"
        )
        fig.update_layout(
            xaxis=dict(tickmode="array", tickformat="%B", title="Mes"),
            yaxis=dict(title="Tendencia Normalizada (0-100)")
        )
        st.plotly_chart(fig)

    elif selected_chart == "Estacionalidad Enero":
        render_month_chart(daily_seasonality, "01-", "Enero")
    elif selected_chart == "Estacionalidad Febrero":
        render_month_chart(daily_seasonality, "02-", "Febrero")
    elif selected_chart == "Estacionalidad Marzo":
        render_month_chart(daily_seasonality, "03-", "Marzo")
    elif selected_chart == "Estacionalidad Abril":
        render_month_chart(daily_seasonality, "04-", "Abril")
    elif selected_chart == "Estacionalidad Mayo":
        render_month_chart(daily_seasonality, "05-", "Mayo")
    elif selected_chart == "Estacionalidad Junio":
        render_month_chart(daily_seasonality, "06-", "Junio")
    elif selected_chart == "Estacionalidad Julio":
        render_month_chart(daily_seasonality, "07-", "Julio")
    elif selected_chart == "Estacionalidad Agosto":
        render_month_chart(daily_seasonality, "08-", "Agosto")
    elif selected_chart == "Estacionalidad Septiembre":
        render_month_chart(daily_seasonality, "09-", "Septiembre")
    elif selected_chart == "Estacionalidad Octubre":
        render_month_chart(daily_seasonality, "10-", "Octubre")
    elif selected_chart == "Estacionalidad Noviembre":
        render_month_chart(daily_seasonality, "11-", "Noviembre")
    elif selected_chart == "Estacionalidad Diciembre":
        render_month_chart(daily_seasonality, "12-", "Diciembre")
    
    #Fuente de datos para calcular el df
    #st.subheader("Datos gráfico de barras")
    #df_porcentaje = pd.read_excel('C:/Users/hector/projects/marcos/mi_dashboard/jupiter_graphs/seasonal_info_euro.xlsx')
    #st.dataframe(df_porcentaje)
    st.subheader("Datos USD de Yahoo Finance")
    st.dataframe(df_visible)

def render_month_chart(daily_seasonality, month_prefix, month_name):
    buy_threshold = 69
    sell_threshold = 31
    month_data = daily_seasonality[daily_seasonality.index.str.contains(month_prefix)]
    options = {
        "title": {"text": f"{month_name} (Daily)", "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {"type": "category", "data": month_data.index.tolist(), "axisLabel": {"rotate": 90}},
        "yAxis": {"type": "value", "name": "Porcentaje"},
        "series": [
            {
                "name": "% Positivo",
                "type": "bar",
                "data": [
                    {
                        "value": val,
                        "itemStyle": {"color": "green" if val > buy_threshold else "red" if val < sell_threshold else "blue",
                                      "opacity": 1.0 if val > buy_threshold else 1.0 if val < sell_threshold else 0.6}
                    }
                    for val in month_data['Percentage_Positive']
                ],
                "label": {"show": True, "position": "top", "formatter": "{c}%"}
            }
        ]
    }
    st_echarts(options=options, height="500px")
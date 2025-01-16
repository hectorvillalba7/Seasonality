import datetime as dt
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_echarts import st_echarts

def run():
    st.title("Seasonality of Pound futures")

    ticker = "6B=F"

    # date selection
    start = st.date_input("Starting Date", value=dt.datetime(2001, 1, 1))
    end = st.date_input("End Date", value=dt.datetime.now())

    if start >= end:
        st.error("Starting date must be previous to end date.")
        return

    # Download data from yahoof
    with st.spinner("Downloading data"):
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
        st.error("There is no data for the selected time.")
        return
    
    # Calculate columns for seasonality line plot
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

    # Group data for bar plots
    df_visible['Date'] = pd.to_datetime(df_visible['Date'])
    df_visible['Month-day'] = df_visible['Date'].dt.strftime("%m-%d")
    df_visible['Return'] = df_visible['Close'].pct_change().fillna(0)
    daily_seasonality = df_visible.groupby('Month-day').agg(
        count=('Return', 'count'),
        positive=('Return', lambda x: (x > 0).sum()),
        average_gain_loss=('Return', lambda x: x.mean())
    )

    # ---------------------plotly Line plot-----------------------

    st.subheader("Seasonality chart")
    fig = px.line(
        grouped_df,
        x="M-D",
        y="normalized",
        title="Seasonality of Pound 6B=F",
        template="simple_white",
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickformat="%B", 
            title="Mes"
        ),
        yaxis=dict(title="Normalized Y (0-100)")
    )
    # Show plot
    fig.update_traces(connectgaps=True)
    st.plotly_chart(fig)

   #---------------------Bar chart divided per month.---------------------

    daily_seasonality['Percentage_Positive'] = (daily_seasonality['positive'] / daily_seasonality['count']) * 100
    daily_seasonality['Percentage_Positive'] = daily_seasonality['Percentage_Positive'].round(2)

    #selectbox
    options = ["Seasonality January", "Seasonality February", "Seasonality March","Seasonality April","Seasonality May", "Seasonality June", "Seasonality July", "Seasonality August","Seasonality September", "Seasonality October", "Seasonality November", "Seasonality December"]
    selected_chart = st.selectbox("Selecciona el gráfico a mostrar:", options)

    # Show selected chart
    if selected_chart == "Seasonal chart":
        fig = px.line(
            grouped_df,
            x="M-D",
            y="normalized",
            title="Seasonality of Pound 6B=F",
            template="simple_white"
        )
        fig.update_layout(
            xaxis=dict(tickmode="array", tickformat="%B", title="Mes"),
            yaxis=dict(title="Normalized Y (0-100)")
        )
        st.plotly_chart(fig)

    elif selected_chart == "Seasonality January":
        render_month_chart(daily_seasonality, "01-", "January")
    elif selected_chart == "Seasonality February":
        render_month_chart(daily_seasonality, "02-", "February")
    elif selected_chart == "Seasonality March":
        render_month_chart(daily_seasonality, "03-", "March")
    elif selected_chart == "Seasonality April":
        render_month_chart(daily_seasonality, "04-", "April")
    elif selected_chart == "Seasonality May":
        render_month_chart(daily_seasonality, "05-", "May")
    elif selected_chart == "Seasonality June":
        render_month_chart(daily_seasonality, "06-", "June")
    elif selected_chart == "Seasonality July":
        render_month_chart(daily_seasonality, "07-", "July")
    elif selected_chart == "Seasonality August":
        render_month_chart(daily_seasonality, "08-", "August")
    elif selected_chart == "Seasonality September":
        render_month_chart(daily_seasonality, "09-", "September")
    elif selected_chart == "Seasonality October":
        render_month_chart(daily_seasonality, "10-", "October")
    elif selected_chart == "Seasonality November":
        render_month_chart(daily_seasonality, "11-", "November")
    elif selected_chart == "Seasonality December":
        render_month_chart(daily_seasonality, "12-", "December")
    
  #Data source to create the charts
    st.subheader("Pound Data from Yahoo Finance")
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


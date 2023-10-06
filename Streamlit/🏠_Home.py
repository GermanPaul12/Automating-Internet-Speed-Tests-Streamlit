import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Internet Speed Hafenstraße',page_icon='🏠')
conn = st.experimental_connection("gsheets", type=GSheetsConnection)


df = conn.read(
    ttl="10m",  # Time to cache the data
    usecols=[0, 1, 2, 3, 4, 5],)  # Which columns to read
    #nrows=3) # How many rows to read
# returns DataFrame

st.title("Internet Speed Hafenstraße")
st.write("Every hour the dataset is updated with the current internet speed")
#print(df.columns.tolist())

for i in df.columns.tolist():
    if i not in ["Time","Date"]:
        df[f"{i}"] = df[f"{i}"].astype(float)
df.Time = pd.to_datetime(df['Time'])

st.write(df)

st.header("Ping")
ping_figure = px.line(df, x="Time", y="Ping in ms", title="Ping Speed in ms Hafenstraße")
st.plotly_chart(ping_figure)

st.header("Download and Upload Speed")
speed_figure = px.line(df, x="Time", y=["Download in Mbit/s", "Upload in Mbit/s"], title="Downlaod and Upload Speed in Mbit/s Hafenstraße")
st.plotly_chart(speed_figure)
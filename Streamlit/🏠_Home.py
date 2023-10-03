import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Internet Speed Hafenstraße',page_icon='🏠')
conn = st.experimental_connection("gsheets", type=GSheetsConnection)


df = conn.read(
    ttl="10m",  # Time to cache the data
    usecols=[0, 1, 2, 3],)  # Which columns to read
    #nrows=3) # How many rows to read
# returns DataFrame

st.title("Internet Speed Hafenstraße")
st.write("Every hour the dataset is updated with the current internet speed")
#print(df.columns.tolist())

for i in df.columns.tolist():
    if i != "Time":
        df[f"{i}"] = df[f"{i}"].astype(float)
df.Time = pd.to_datetime(df['Time'])

st.write(df)

st.header("Ping")
st.plotly_chart(df.plot(x="Time", y="Ping in ms", title="Internet Speed Hafenstraße", xlabel="Date", ylabel="Ping in ms", grid=True, figsize=(10, 5), rot=45))

st.header("Download and Upload Speed")
st.plotly_chart(df.plot(x="Time", y=["Download in Mbit/s", "Upload in Mbit/s"], title="Internet Speed Hafenstraße", xlabel="Date", ylabel="Speed in Mbit/s", grid=True, figsize=(10, 5), rot=45))
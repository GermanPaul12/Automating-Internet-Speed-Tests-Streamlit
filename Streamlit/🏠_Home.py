import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Internet Speed Hafenstraße',page_icon='🏠')
conn = st.experimental_connection("gsheets", type=GSheetsConnection)


df = conn.read(
    ttl="10m",  # Time to cache the data
    usecols=[0, 1, 2, 3],)  # Which columns to read
    #nrows=3) # How many rows to read
# returns DataFrame

st.title("Internet Speed Hafenstraße")
st.write("Every hour the dataset is updated with the current internet speed")

st.write(df)
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
import re
import datetime as dt

#os.system("speedtest-cli > speed.txt")

os.system("speedtest-cli --secure > speed.txt")
new_row = []
now = dt.datetime.now()
# Create a connection object.
conn = st.experimental_connection("gsheets", type=GSheetsConnection)


df = conn.read(
    ttl="10m",  # Time to cache the data
    usecols=[0, 1, 2, 3],)  # Which columns to read
    #nrows=3) # How many rows to read
# returns DataFrame
    
pattern = r"\d+\.\d+ Mbit/s"
pattern_ping = r"\d+\.\d+ ms"

with open("speed.txt", "r") as f:
    data = f.readlines() 

if len(data) >= 9:
    ping = re.search(pattern_ping, data[4])
    download = re.search(pattern, data[6])
    upload = re.search(pattern, data[8])
    if ping:
        print("Ping: ", ping.group())
        new_row.append(ping.group())
    if download:
        print("Download: ", download.group())
        new_row.append(download.group())
    if upload:
        print("Upload: ", upload.group())
        new_row.append(upload.group())
new_row.append(now.strftime(r"%d/%m/%Y %H:%M:%S"))

df.loc[len(df)] = new_row

df.to_csv("backup.csv", index=False)
    
conn.update(data=df) # Update the data with a given DataFrame.
# Print results.    
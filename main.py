import os
import re
import subprocess
import time
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
# Guide https://pimylifeup.com/raspberry-pi-internet-speed-monitor/

response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

try:
    f = open('/home/german/Documents/Coding/Automating-Internet-Speed-Tests-Streamlit/backup.csv', 'a+')
    if os.stat('/home/german/Documents/Coding/Automating-Internet-Speed-Tests-Streamlit/backup.csv').st_size == 0:
            f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
except:
    pass

f.write('{},{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload))

conn = st.experimental_connection("gsheets", type=GSheetsConnection)


df = conn.read(
    ttl="10m",  # Time to cache the data
    usecols=[0, 1, 2, 3, 4, 5],)  # Which columns to read
    #nrows=3) # How many rows to read
# returns DataFrame
df.loc[len(df)] = [time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload]


conn.update(data=df) # Update the data with a given DataFrame.
# Print results.
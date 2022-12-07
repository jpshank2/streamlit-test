import streamlit as st
import numpy as np
import pandas as pd
import snowflake.connector

st.write("# Hello, build! :wave:")

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT TOP 10 * FROM BMSS_SSMS_JSON;")

for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
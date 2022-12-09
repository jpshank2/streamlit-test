import streamlit as st
import numpy as np
import pandas as pd
import snowflake.connector

st.write("# Hello, wip! :wave:")

#@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    conn = init_connection()

    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

try:
    rows = run_query("SELECT TOP 10 * FROM SSMS_JSON;")

    for row in rows:
        st.write(f"{row[0]} has a :{row[1]}:")

except Exception as e:
    st.write(e)

finally:
    conn.close()
import streamlit as st
import numpy as np
import pandas as pd
import snowflake.connector

st.write("# Hello, AR! :wave:")

@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

@st.cache_data(ttl=3600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return pd.DataFrame(cur.fetchall())

rows = run_query("SELECT top 10 * from TRANS_AR AR INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")


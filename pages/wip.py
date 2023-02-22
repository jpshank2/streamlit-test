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
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        results = list
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return pd.DataFrame(results)

try:
    rows = run_query("SELECT top 10 * from TRANS_AR AR INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex;")

    # Print results.
    # st.dataframe(rows)

    for row in rows:
        st.write(f"{row}")
except Exception as e:
    print(st.write(e))

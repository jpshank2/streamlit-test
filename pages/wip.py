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
        results = list()
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return pd.DataFrame(results)

try:
    rows = run_query("SELECT * from TRANS_AR AR INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex;")

    # Print results.
    st.write(rows.columns)

    office_AR = rows[['OFFICE', 'DEBTTRANUNPAID']].copy()
    office_AR = office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
    st.bar_chart(office_AR, x='OFFICE', y='OUTSTANDING_AR')

    partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
    partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
    partner_AR = partner_AR[partner_AR['OUSTANDING_AR'] != 0]
    st.bar_chart(partner_AR, x='CLIENTPARTNER', y='OUTSTANDING_AR')
except Exception as e:
    print(st.write(e))

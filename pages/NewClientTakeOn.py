import streamlit as st
from snowflake.connector import connect
from automations.ncto.frame import clientTakeOn
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st, conn)

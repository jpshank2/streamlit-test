import streamlit as st
import snowflake.connector
from automations.ncto.frame import clientTakeOn
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

st.write("<h1>This is HTML</h1>", unsafe_allow_html=True)
st.markdown("## Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st, conn)

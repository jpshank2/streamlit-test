import streamlit as st
from snowflake.connector import connect
from automations.ncto.frame import clientTakeOn
from utilities.queries import run_query
from PIL import Image
from requests import get
from io import BytesIO
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

if 'pageCounter' not in st.session_state:
    st.session_state['pageCounter'] = 0
if 'valid' not in st.session_state:
    st.session_state['valid'] = [True]
if 'clicks' not in st.session_state:
    st.session_state['clicks'] = [0]
if 'offices' not in st.session_state:
    st.session_state['offices'] = run_query('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;', conn)
if 'clients' not in st.session_state:
    st.session_state['clients'] = run_query("SELECT CLIENT, CLIENTDISPLAY, CODE, CONTINDEX FROM DIM_CLIENT_MASTER;", conn)
if 'staff' not in st.session_state:
    st.session_state['staff'] = run_query("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'Active' AND DEPARTMENT <> 'No Selection';", conn)
if 'entities' not in st.session_state:
    st.session_state['entities'] = run_query("SELECT * FROM DIM_ENTITIES;", conn)
if 'industries' not in st.session_state:
    st.session_state['industries'] = run_query("SELECT * FROM DIM_INDUSTRIES WHERE ACTIVE = true;", conn)
if 'contacts' not in st.session_state:
    st.session_state['contacts'] = run_query("SELECT * FROM DIM_CONTACTS WHERE CONTTYPE = 1;", conn)
if 'newclient' not in st.session_state:
    st.session_state['newclient'] = {'general': [], 'client': [], 'contact': [], 'billings': [], 'attributes': [], 'services': []}

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/DcFwdrQ.png').content))

#Added a logo to the top of the screen
st.image(MainHeaderImage, use_column_width = True)

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st)

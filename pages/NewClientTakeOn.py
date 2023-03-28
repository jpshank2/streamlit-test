import streamlit as st
from snowflake.connector import connect
from automations.ncto.frame import clientTakeOn
from utilities.queries import get_rows
from PIL import Image
from requests import get
from io import BytesIO
# import automations.ncto.frame as ncto


@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

# conn = init_connection()
if 'conn' not in st.session_state:
    st.session_state['conn'] = init_connection()
if 'pageCounter' not in st.session_state:
    st.session_state['pageCounter'] = 0
if 'valid' not in st.session_state:
    st.session_state['valid'] = [True]
if 'clicks' not in st.session_state:
    st.session_state['clicks'] = [0]
if 'offices' not in st.session_state:
    st.session_state['offices'] = get_rows('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;')
if 'clients' not in st.session_state:
    st.session_state['clients'] = get_rows("SELECT CLIENT, CLIENTDISPLAY, CODE, CONTINDEX, STATUS, ORIGINATOR, strtok_to_array(code, '-')[0]::string parent, strtok_to_array(code, '-')[1]::string child FROM DIM_CLIENT_MASTER;")
if 'staff' not in st.session_state:
    st.session_state['staff'] = get_rows("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'Active' AND DEPARTMENT <> 'No Selection';")
if 'entities' not in st.session_state:
    st.session_state['entities'] = get_rows("SELECT * FROM DIM_ENTITIES;")
if 'industries' not in st.session_state:
    st.session_state['industries'] = get_rows("SELECT * FROM DIM_INDUSTRIES WHERE ACTIVE = true;")
if 'contacts' not in st.session_state:
    st.session_state['contacts'] = get_rows("SELECT * FROM DIM_CONTACTS WHERE CONTTYPE = 1;")
if 'services' not in st.session_state:
    st.session_state['services'] = get_rows("SELECT * FROM DIM_SERVICES WHERE SERVNON = FALSE")
if 'newclient' not in st.session_state:
    st.session_state['newclient'] = {'general': [], 'client': [], 'contact': [], 'billings': [], 'attributes': [], 'services': [], 'review': []}

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/DcFwdrQ.png').content))

#Added a logo to the top of the screen
st.image(MainHeaderImage, use_column_width = True)

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st)
st.write(st.session_state.clients)

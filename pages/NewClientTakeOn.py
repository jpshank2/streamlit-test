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
if 'offices' not in st.session_state:
    st.session_state['offices'] = run_query('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;', conn)
if 'clients' not in st.session_state:
    st.session_state['clients'] = run_query("SELECT * FROM DIM_CLIENT_MASTER WHERE STATUS <> 'LOST';", conn)
if 'staff' not in st.session_state:
    st.session_state['staff'] = run_query("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'ACTIVE' AND DEPARTMENT <> 'No Selection';", conn)
    
MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/DcFwdrQ.png')))

#Added a logo to the top of the screen
st.image(MainHeaderImage, use_column_width = True)

st.markdown("# Hello, form! :wave:")
# ncto.clientTakeOn(st, conn)
clientTakeOn(st)

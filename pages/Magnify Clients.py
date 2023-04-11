import streamlit as st
from automations.ncto.frame import clientTakeOn
from utilities.queries import get_rows, init_connection
from utilities.loading_screen import loading
from PIL import Image
from requests import get
from io import BytesIO
from json import loads

st.set_page_config(
    page_title='Magnify | Clients',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
)

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
st.image(MainHeaderImage, use_column_width = True)

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    st.markdown("# Hello, form! :wave:")
    # ncto.clientTakeOn(st, conn)

    with st.spinner('Loading necessary New Client Take On data...'):
        if 'conn' not in st.session_state:
            st.session_state['conn'] = init_connection()
        if 'pageCounter' not in st.session_state:
            st.session_state['pageCounter'] = 0
        if 'valid' not in st.session_state:
            st.session_state['valid'] = [True]
        if 'switches' not in st.session_state:
            domain = 'demo' if st.experimental_user.email == None else st.experimental_user.email.split('@')[-1]
            st.session_state['switches'] = get_rows(f"SELECT * FROM STREAMLITAPP.MANAGED_IDENTITY_TEST WHERE DOMAIN = '{domain}';")
        if 'offices' not in st.session_state:
            st.session_state['offices'] = get_rows('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;')
        if 'clients' not in st.session_state:
            st.session_state['clients'] = get_rows("SELECT CLIENT, CLIENTDISPLAY, CODE, CONTINDEX, STATUS, OFFICE, ORIGINATOR, strtok_to_array(code, '-')[0]::string parent, strtok_to_array(code, '-')[1]::string child FROM DIM_CLIENT_MASTER WHERE NOT RLIKE(CODE, '.*[a-z].*', 'i');")
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
            st.session_state['newclient'] = loads(st.session_state['switches'].CLIENT_SESSION.iloc[0])#{'general': [], 'client': [], 'contact': [], 'billings': [], 'attributes': [], 'services': [], 'review': []}

    clientTakeOn(st)

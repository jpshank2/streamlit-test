import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading

st.set_page_config(
    page_title='Power BI Starter Pack',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

# MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
# one, two, three= st.columns(3)
# two.image(MainHeaderImage, use_column_width = True)
if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    
    for session in list(st.session_state.key()):
        if session not in st.session_state['master_states']:
            del st.session_state[session]

    st.write('<iframe src="https://api.bmss.com/cpa" width="1500" height="900"></iframe>', unsafe_allow_html=True)
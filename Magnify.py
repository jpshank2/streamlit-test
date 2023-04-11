#
# streamlit docs can be found here: https://docs.streamlit.io/
#

import streamlit as st
from utilities.loading_screen import loading
from PIL import Image
from requests import get
from io import BytesIO

st.set_page_config(
    page_title='Magnify | Home',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
st.image(MainHeaderImage)#, use_column_width = True)

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    st.markdown(f"# Welcome to Magnify, {st.session_state['user']['EMPLOYEE'].iloc[0]}!")

    # st.markdown(f"## Hello, {st.session_state['user']['EMPLOYEE'].iloc[0] if not st.session_state['user'].empty else 'Test User'}! :wave:")

    st.markdown("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")
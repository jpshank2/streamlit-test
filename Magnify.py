#
# streamlit docs can be found here: https://docs.streamlit.io/
#

import streamlit as st
from utilities.loading_screen import loading
from PIL import Image
from requests import get
from io import BytesIO

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/2ffgLBo.png').content))
st.image(MainHeaderImage, use_column_width = True)

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    st.markdown(f"# Welcome to Magnify, {st.session_state['user']['EMPLOYEE'].iloc[0]}!")

    # st.markdown(f"## Hello, {st.session_state['user']['EMPLOYEE'].iloc[0] if not st.session_state['user'].empty else 'Test User'}! :wave:")

    st.markdown("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")
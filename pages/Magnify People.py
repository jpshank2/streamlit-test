import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO

st.set_page_config(
    page_title='Magnify | People',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
)

st.markdown('eventual m+m page')
import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO

st.set_page_config(
    page_title='Power BI Starter Pack',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

# MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
# one, two, three= st.columns(3)
# two.image(MainHeaderImage, use_column_width = True)

st.write('<iframe src="https://api.bmss.com/cpa" width="1500" height="900"></iframe>', unsafe_allow_html=True)
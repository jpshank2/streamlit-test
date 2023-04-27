import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading
from utilities.queries import get_rows
from utilities.click_handlers import fill_request, submit_review
from datetime import datetime
from plotly.express import pie

st.set_page_config(
    page_title='Magnify | Morale',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
one, two, three= st.columns(3)
two.image(MainHeaderImage, use_column_width = True)


if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    st.markdown('# Magnify Morale')

    with st.form('morale_form'):
        st.markdown('## Rate your morale within your team:')
        st.radio('I am enthusiastic about the owth that I do for my team', (1, 2, 3, 4, 5, 6, 7))
        st.radio('I find the work that I do for my team of meaning and purpose', (1, 2, 3, 4, 5, 6, 7))
        st.radio('I am proud of the work that I do for my team', (1, 2, 3, 4, 5, 6, 7))
        st.radio('To me, the work that I do for my team is appropriately challenging', (1, 2, 3, 4, 5, 6, 7))
        st.radio('I am energized by working with my team', (1, 2, 3, 4, 5, 6, 7))
        st.radio('In my team, I feel fit and strong', (1, 2, 3, 4, 5, 6, 7))
        st.radio('In my team, I quickly recover from setbacks', (1, 2, 3, 4, 5, 6, 7))
        st.radio('In my team, I can keep going for a long time', (1, 2, 3, 4, 5, 6, 7))
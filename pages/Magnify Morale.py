import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading

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
    
    # for session in list(st.session_state.keys()):
    #     if session not in st.session_state['master_states']:
    #         del st.session_state[session]

    st.markdown('# Magnify Morale')

    with st.form('morale_form', clear_on_submit=True):
        st.markdown('## Rate your morale within your team:')
        st.radio('I am enthusiastic about the work that I do for my team', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('I find the work that I do for my team of meaning and purpose', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('I am proud of the work that I do for my team', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('To me, the work that I do for my team is appropriately challenging', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('I am energized by working with my team', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('In my team, I feel fit and strong', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('In my team, I quickly recover from setbacks', (1, 2, 3, 4, 5, 6, 7), horizontal=True)
        st.radio('In my team, I can keep going for a long time', (1, 2, 3, 4, 5, 6, 7), horizontal=True)

        st.form_submit_button('Submit')
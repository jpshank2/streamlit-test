import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading
from utilities.queries import get_rows

st.set_page_config(
    page_title='Magnify | People',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
one, two, three= st.columns(3)
two.image(MainHeaderImage, use_column_width = True)


if 'company' not in st.session_state:
    loading(st)

if 'staff' not in st.session_state:
    st.session_state['staff'] = get_rows("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'Active' AND DEPARTMENT <> 'No Selection';")

if 'company' in st.session_state:
    review, request = st.columns(2)
    with review.form('review_form', clear_on_submit=True):
        st.text_input('What Job or Project are you reviewing?', key='review_project')
        st.selectbox('Select an employee', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='review_employee')
        st.radio('How did this employee do on the project?', ('Thumb\'s up', 'Okay', 'Thumb\'s down'), key='review_rating', horizontal=True)
        st.text_area('See more', placeholder='What did this employee do well that you\'d like to see more?', key='review_more')
        st.text_area('See less', placeholder='What did this employee do that you\'d like to see less?', key='review_less')
        st.form_submit_button('Submit', type='primary')
    
    with request.form('request_from', clear_on_submit=True):
        st.selectbox('Select an employee', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='request_employee')
        st.text_input('What Job or Project?', key='request_project')
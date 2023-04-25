import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading
from utilities.queries import get_rows
from datetime import datetime
from plotly.express import pie

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
        st.markdown('#### Review a fellow staff')
        st.selectbox('Staff to review', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='review_employee')
        st.text_input('What Job or Project are you reviewing?', key='review_project')
        st.radio('How did this employee do on the project?', ('Thumbs up', 'Okay', 'Thumbs down'), key='review_rating', horizontal=True)
        st.text_area('See more', placeholder='What did this employee do well that you\'d like to see more?', key='review_more')
        st.text_area('See less', placeholder='What did this employee do that you\'d like to see less?', key='review_less')
        st.form_submit_button('Submit', type='primary')
    
    with request.form('request_from', clear_on_submit=True):
        st.markdown('#### Request a review')
        st.selectbox('Staff to be reviewed by', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='request_employee')
        st.text_input('What Job or Project?', key='request_project')
        st.form_submit_button('Request a Review')

    request.markdown('#### Outstanding requests:')

    st.markdown('#### My Reviews:')
    fym = 5
    fye = st.session_state['today'].year if st.session_state['today'].month < fym else st.session_state['today'].year + 1

    review_table, review_pie = st.columns([2, 1])

    reviews = get_rows(f"""select r.Date,
        r.project,
        s.staff_name as Sender,
        r.rating,
        r.see_more,
        r.see_less
    from people.review r
        inner join dim_staff_master s on s.staffindex = r.sender
    where r.recipient = {st.session_state['user']['STAFFINDEX'].iloc[0]}
        AND r.Date BETWEEN '{datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')}' AND '{datetime(fye, fym, 1)}';""")
    
    review_table.dataframe(reviews, use_container_width=True)

    review_pie = pie(reviews, values=reviews.value_counts('RATING'), names='RATING')

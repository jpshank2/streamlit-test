import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading
from utilities.queries import get_rows
from utilities.click_handlers import fill_request
from utilities.validators import validate_dropdown, validate_string
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
    if 'req_link' not in st.session_state:
        st.session_state['req_link'] = 0

    if 'staff_select' not in st.session_state:
        st.session_state['staff_select'] = [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFINDEX'] != st.session_state['user']['STAFFINDEX'].iloc[0]].EMPLOYEE]

    if 'project_input' not in st.session_state:
        st.session_state['project_input'] = ''

    if 'review_valid' not in st.session_state:
        st.session_state['review_valid']= [False for i in range(4)]
    request_valid = [False for i in range(2)]

    review, request = st.columns(2)
    with review.form('review_form', clear_on_submit=True):
        st.markdown('#### Review a fellow staff')
        st.selectbox('Staff to review', st.session_state['staff_select'], key='review_employee')
        st.session_state['review_valid'][0] = validate_dropdown(st.session_state['review_employee'], [''])

        st.text_input('What Job or Project are you reviewing?', value=st.session_state['project_input'], key='review_project')
        st.session_state['review_valid'][1] = validate_string(st.session_state['review_project'], [''])
        
        st.radio('How did this staff do on the project?', ('Thumbs up', 'Okay', 'Thumbs down'), key='review_rating', horizontal=True)
        
        review_more = st.text_area('See more')#, placeholder='What did this co-worker do well that you\'d like to see more?')
        st.write(review_more)
        st.session_state['review_valid'][2] = validate_string(review_more, [''])
        
        review_less = st.text_area('See less', placeholder='What did this co-worker do that you\'d like to see less?', key='review_less')
        # st.session_state['review_valid'][3] = validate_string(st.session_state['review_less'], [''])

        st.write(st.session_state['review_valid'])
        
        st.form_submit_button('Submit', type='primary', disabled=(False in st.session_state['review_valid']))
    
    with request.form('request_from', clear_on_submit=True):
        st.markdown('#### Request a review')
        st.selectbox('Staff to be reviewed by', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='request_employee')
        st.text_input('What Job or Project?', key='request_project')
        st.form_submit_button('Request a Review')

    recieved_requests = get_rows(f"""select R.DATE
        ,S.EMPLOYEE
        ,R.PROJECT
        ,R.IDX
    from people.requests R
        INNER JOIN dim_staff_master S ON S.STAFFINDEX = R.SENDER
    WHERE R.REVIEW_LINK IS NULL
        AND R.RECIPIENT = {st.session_state['user']['STAFFINDEX'].iloc[0]}
    ORDER BY R.DATE;""")

    request.markdown('#### My Recieved Outstanding Requests:')

    review_request, this_request, remove_request = request.columns([1, 3, 1])

    if recieved_requests.empty:
        request.markdown('No outstanding receieved requests!')
    else:
        for i in range(recieved_requests.shape[0]):
            review_request.button(":heavy_check_mark:", help='Fill out this requested review!', key=f'review_{i}', on_click=fill_request(recieved_requests.iloc[i], st.session_state))
            this_request.markdown(f"**{recieved_requests.iloc[i]['PROJECT']}** from **{recieved_requests.iloc[i]['EMPLOYEE']}**")
            remove_request.button(":x:", help='Remove this requested review', key=f'remove_{i}')

    sent_requests = get_rows(f"""select R.DATE
        ,S.EMPLOYEE
        ,R.PROJECT
    from people.requests R
        INNER JOIN dim_staff_master S ON S.STAFFINDEX = R.RECIPIENT
    WHERE R.REVIEW_LINK IS NULL
        AND R.SENDER = {st.session_state['user']['STAFFINDEX'].iloc[0]}
    ORDER BY R.DATE;""")
    
    request.markdown('#### My Sent Outstanding Requests')
    if sent_requests.empty:
        request.markdown('No outstanding sent requests!')
    else:
        request.dataframe(sent_requests)

    st.markdown('#### My Reviews:')
    fym = 5
    fye = st.session_state['today'].year if st.session_state['today'].month < fym else st.session_state['today'].year + 1

    review_pie, review_table = st.columns([3, 4])

    reviews = get_rows(f"""select r.Date,
        r.project,
        s.employee as Sender,
        r.rating,
        r.see_more,
        r.see_less
    from people.review r
        inner join dim_staff_master s on s.staffindex = r.sender
    where r.recipient = {st.session_state['user']['STAFFINDEX'].iloc[0]}
        AND r.Date BETWEEN '{datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')}' AND '{datetime(fye, fym, 1)}'
    ORDER BY R.DATE;""")
    
    review_table.dataframe(reviews, use_container_width=True)

    review_pie_df = reviews.groupby('RATING', as_index=False).agg(TOTAL=('RATING', 'count')).reset_index()

    review_pie.plotly_chart(pie(review_pie_df, values='TOTAL', names='RATING').update_layout({'legend_orientation': "h"}))

    review_pie_df = None

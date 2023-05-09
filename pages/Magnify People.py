import streamlit as st
from PIL import Image
from requests import get
from io import BytesIO
from utilities.loading_screen import loading
from utilities.queries import get_rows, get_new_data
from utilities.click_handlers import submit_review
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

def fill_request(selection, requests):

    df = requests[requests['REQUEST_STRING'] == selection]

    staff = df['EMPLOYEE'].iloc[0]
    st.session_state['staff_select'] = [staff]
    # st.session_state['review_employee'] = [staff]
    project = df['PROJECT'].iloc[0]
    st.session_state['project_input'] = project

    st.session_state['req_link'] = df['IDX'].iloc[0]

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    
    # for session in list(st.session_state.keys()):
    #     if session not in st.session_state['master_states']:
    #         del st.session_state[session]

    requests = get_new_data(f"""select R.DATE
            ,S.EMPLOYEE
            ,R.PROJECT
            ,R.IDX
            ,CONCAT(r.project, ' from ', s.employee) as request_string
        from people.requests R
            INNER JOIN PE.DIM_ANON_STAFF S ON S.STAFFINDEX = R.SENDER
        WHERE R.REVIEW_LINK IS NULL
            AND R.RECIPIENT = {st.session_state['user']['STAFFINDEX'].iloc[0]}
        ORDER BY R.DATE;""")

    st.markdown('# Magnify People')

    if 'req_link' not in st.session_state:
        if 'review_request' not in st.session_state or st.session_state['review_request'] == 'New':
            st.session_state['req_link'] = 0
        else:
            st.session_state['req_link'] = requests[requests['REQUEST_STRING'] == st.session_state['review_request']].iloc[0].IDX

    if 'staff_select' not in st.session_state:
        if 'review_request' not in st.session_state or st.session_state['review_request'] == 'New':
            st.session_state['staff_select'] = [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFINDEX'] != st.session_state['user']['STAFFINDEX'].iloc[0]].EMPLOYEE]
        else:
            st.session_state['staff_select'] = [requests[requests['REQUEST_STRING'] == st.session_state['review_request']].iloc[0].EMPLOYEE]

    if 'project_input' not in st.session_state:
        if 'review_request' not in st.session_state or st.session_state['review_request'] == 'New':
            st.session_state['project_input'] = ''
        else:
            st.session_state['project_input'] = [requests[requests['REQUEST_STRING'] == st.session_state['review_request']].iloc[0].PROJECT]

    review, request = st.columns(2)
    # with review.form('review_form', clear_on_submit=True):
    review.markdown('#### Review a fellow staff')
    review.selectbox('Staff to review', st.session_state['staff_select'], key='review_employee')

    review.text_input('What Job or Project are you reviewing?', value=st.session_state['project_input'], key='review_project')

    if not requests.empty:
        review.markdown(' -- OR --')

        review.selectbox('Select a requested review', ['New'] + [i for i in requests.REQUEST_STRING], key='review_request')
    
    review.radio('How did this staff do on the project?', ('Thumbs up', 'Okay', 'Thumbs down'), key='review_rating', horizontal=True)
    
    review.text_area('See more', placeholder='What did this co-worker do well that you\'d like to see more?', key='review_more')

    review.text_area('See less', placeholder='What did this co-worker do that you\'d like to see less?', key='review_less')

    review.button('Submit', key='review_submit')

    review.write(st.session_state)
        
        # st.form_submit_button('Submit', type='primary', on_click=submit_review, kwargs={'session': st.session_state})
    
    with request.form('request_from', clear_on_submit=True):
        st.markdown('#### Request a review')
        st.selectbox('Staff to be reviewed by', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='request_employee')
        st.text_input('What Job or Project?', key='request_project')
        st.form_submit_button('Request a Review')

    # if 'received_requests' not in st.session_state:
        #st.session_state['received_requests'] 

    # request.markdown('#### My Received Outstanding Requests:')

    # review_request, this_request, remove_request = request.columns([1, 3, 1])

    # if requests.empty:
    #     request.markdown('No outstanding receieved requests!')
    # else:
    #     recieve_options = (i[1][4] for i in requests.iterrows())
    #     with request.form('received_requests'):
    #         outstanding_receieved = st.radio('hidden label', options=recieve_options, label_visibility='hidden')
    #         st.form_submit_button('Review this Request', on_click=fill_request, args=(outstanding_receieved, requests))
        # for i in range(st.session_state['received_requests'].shape[0]):
            # create_requests_with_button(i)

    sent_requests = get_rows(f"""select R.DATE
        ,S.EMPLOYEE
        ,R.PROJECT
    from people.requests R
        INNER JOIN PE.DIM_ANON_STAFF S ON S.STAFFINDEX = R.RECIPIENT
    WHERE R.REVIEW_LINK IS NULL
        AND R.SENDER = {st.session_state['user']['STAFFINDEX'].iloc[0]}
    ORDER BY R.DATE;""", st.session_state['today'])
    
    request.markdown('#### My Sent Outstanding Requests')
    if sent_requests.empty:
        request.markdown('No outstanding sent requests!')
    else:
        request.dataframe(sent_requests)

    st.markdown('#### My Reviews:')

    review_pie, review_table = st.columns([3, 4])

    reviews = get_rows(f"""select r.Date,
        r.project,
        s.employee as Sender,
        r.rating,
        r.see_more,
        r.see_less
    from people.review r
        inner join PE.DIM_ANON_STAFF s on s.staffindex = r.sender
    where r.recipient = {st.session_state['user']['STAFFINDEX'].iloc[0]}
        AND r.Date BETWEEN '{datetime(st.session_state['fye'] - 1, st.session_state['company'].FISCAL_MONTH.iloc[0], 1).strftime('%Y-%m-%d')}' AND '{datetime(st.session_state['fye'], st.session_state['company'].FISCAL_MONTH.iloc[0], 1)}'
    ORDER BY R.DATE;""", st.session_state['today'])
    
    review_table.dataframe(reviews, use_container_width=True)

    review_pie_df = reviews.groupby('RATING', as_index=False).agg(TOTAL=('RATING', 'count')).reset_index()

    review_pie.plotly_chart(pie(review_pie_df, values='TOTAL', names='RATING').update_layout({'legend_orientation': "h"}))

    review_pie_df = None

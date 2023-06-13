#
# streamlit docs can be found here: https://docs.streamlit.io/
#

import streamlit as st
# from streamlit.web.server.websocket_headers import _get_websocket_headers
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
one, two, three= st.columns(3)
two.image(MainHeaderImage, use_column_width = True)

# headers = _get_websocket_headers()
# if "X-Ms-Client-Principal-Name" in headers:
#     user_email = headers["X-Ms-Client-Principal-Name"]
#     st.write(f"logged in user is {user_email}")

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    
    # for session in list(st.session_state.keys()):
    #     if session not in st.session_state['master_states']:
    #         del st.session_state[session]

    st.markdown(f"# Welcome to Magnify, {st.session_state['user']['EMPLOYEE'].iloc[0]}!")

    # if st.session_state['user'].EMPLOYEE.iloc[0] == 'Fawn Smith':
    level_pick = st.selectbox('Pick a level to view as:', ['No Selection', 'Member', 'Senior Manager', 'Manager', 'Supervisor', 'Senior', 'Staff', 'Intern', 'Admin'], key='level_pick')
    if level_pick == 'Member':
        st.session_state['level'] = 4
    # elif level_pick == 'Senior Manager':
    #     st.session_state['level'] = 3
    # elif level_pick == 'Manager' or level_pick == 'Supervisor':
    #     st.session_state['level'] = 2
    else:
        st.session_state['level'] = 1

    st.markdown("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")
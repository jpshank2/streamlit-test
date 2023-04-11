#
# streamlit docs can be found here: https://docs.streamlit.io/
#

import streamlit as st
# from utilities.queries import get_rows, init_connection
# from utilities.queries import get_rows
# from snowflake.connector import connect
# 
from utilities.loading_screen import loading

# if 'conn' not in session_state:
#     session_state['conn'] = init_connection()
# if 'user' not in session_state:
#     session_state['user'] = get_rows(f"SELECT * FROM CLIENT_BMSS_SANDBOX_DB.HDS_SSMS_PE.DIM_STAFF_MASTER WHERE STAFF_EMAIL = '{experimental_user.email}'")

if 'company' not in st.session_state:
    loading(st)
    
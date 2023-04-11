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

if 'company' in st.session_state:
    st.markdown(f"# Hello, {st.session_state['user']['EMPLOYEE'].iloc[0] if not st.session_state['user'].empty else 'Test User'}! :wave:")

    st.markdown("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")
else:
    loading(st)
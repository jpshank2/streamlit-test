#
# streamlit docs can be found here: https://docs.streamlit.io/
#

from streamlit import markdown, snow, experimental_user#, cache_resource, secrets, session_state
# from utilities.queries import get_rows
# from snowflake.connector import connect
# 

markdown(f"# Hello, {experimental_user.email if experimental_user.email != None else 'Test User'}! :wave:")
snow()

markdown("This is the Abacus Technologies test site for creating streamlit apps for Business Intelligence. If you are interested in our services, please [email us](mailto:bizintel@abacustechnologies.com?subject=Streamlit).")

#
# beginning work on initializing connection and queries on load - need to find way to always init if not starting at homepage
#
# @cache_resource
# def init_connection():
#     return connect(
#         **secrets["snowflake"], client_session_keep_alive=True
#     )

# conn = init_connection()

# if 'conn' not in session_state:
#         session_state['conn'] = conn
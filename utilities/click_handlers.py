from utilities.queries import insert_rows
from random import randint
from snowflake.connector import connect
# from json import dumps

def create_new_client(st):
    new_client = st.session_state['newclient']

    office = st.session_state.offices[st.session_state.offices.OFFICENAME == new_client['general'][-1]['general_office']].OFFICEINDEX.iloc[0]

    key = str(office) + new_client['general'][-1]['general_client'][:3] + str(randint(0, 999999))
    key = key.replace(' ', '_')

    insert_rows('NCTO', 'ENTERED_CLIENTS', [key, new_client], connect(**st.secrets["snowflake"], client_session_keep_alive=True))

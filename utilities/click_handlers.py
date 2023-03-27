from utilities.queries import run_query
from random import randint
from json import dumps

def create_new_client(st):
    new_client = st.session_state['newclient']
    office = st.session_state.offices[st.session_state.offices.OFFICENAME == new_client[-1]['general_office']].OFFICEINDEX.iloc[0]

    key = str(office) + new_client['general'][-1]['general_client'][:3] + str(randint(0, 999999))
    key = key.replace(' ', '_')

    run_query(f'INSERT INTO NCTO.ENTERED_CLIENTS VALUES ({key}, {dumps(new_client)});')

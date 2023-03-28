from utilities.queries import insert_rows
from random import randint

def create_new_client(st):
    state_client = st.session_state['newclient']

    office = st.session_state.offices[st.session_state.offices.OFFICENAME == state_client['general'][-1]['general_office']].OFFICEINDEX.iloc[0]

    if state_client['general'][-1]['general_type'] == 'New Client Relationship':
        switch = int(st.session_state.staff[st.session_state.staff.EMPLOYEE == state_client['general'][-1]['general_originator']].STAFFINDEX.iloc[0])
    else:
        switch = st.session_state.clients[st.session_state.clients.CLIENTDISPLAY == state_client['general'][-1]['general_relationship']].CODE.iloc[0]

    key = str(office) + state_client['general'][-1]['general_client'][:3] + str(randint(0, 999999))
    key = key.replace(' ', '_')

    new_client = {'generals': {}}#, 'client': {}, 'contact': {}, 'billings': {}}

    new_client['generals']['entry'] = state_client['general'][-1]['general_type']
    new_client['generals']['office'] = state_client['general'][-1]['general_office']
    new_client['generals']['client'] = state_client['general'][-1]['general_client']
    new_client['generals']['switch'] = switch

    st.write(insert_rows('NCTO', 'ENTERED_CLIENTS', [key], new_client))

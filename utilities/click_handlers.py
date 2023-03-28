from utilities.queries import insert_rows
from random import randint
from json import loads

def create_new_client(st):
    state_client = st.session_state['newclient']
    state_switches = st.session_state['switches']

    office = st.session_state.offices[st.session_state.offices.OFFICENAME == state_client['general'][-1]['general_office']].OFFICEINDEX.iloc[0]

    if state_client['general'][-1]['general_type'] == 'New Client Relationship':
        originator = int(st.session_state.staff[st.session_state.staff.EMPLOYEE == state_client['general'][-1]['general_originator']].STAFFINDEX.iloc[0])
        relationship = ''
    else:
        originator = 0
        relationship_code = state_client['general'][-1]['general_relationship'][-10:-5]
        parent_client = st.session_state.clients[st.session_state.clients.PARENT == relationship_code]
        max_child = parent_client.CHILD.astype(int).max()
        relationship = relationship_code + str(max_child + 1).zfill(3)
        # originator = parent_client.ORIGINATOR.iloc[0]
        # st.session_state.clients[st.session_state.clients.CLIENTDISPLAY == state_client['general'][-1]['general_relationship']].CODE.iloc[0]

    key = str(office) + state_client['general'][-1]['general_client'][:3] + str(randint(0, 999999))
    key = key.replace(' ', '_')

    new_client = {'generals': {}}#, 'client': {}, 'contact': {}, 'billings': {}}

    new_client['generals']['entry'] = state_client['general'][-1]['general_type']
    new_client['generals']['office'] = state_client['general'][-1]['general_office']
    new_client['generals']['client'] = state_client['general'][-1]['general_client']
    new_client['generals']['originator'] = originator
    new_client['generals']['relationship'] = relationship
    st.write(state_switches.VALIDATOR_SECTION.iloc[0])
    st.write(state_switches.VALIDATOR_FIELD.iloc[0])
    if state_client[state_switches.VALIDATOR_SECTION.iloc[0]][state_switches.VALIDATOR_FIELD.iloc[0]] in list(loads(state_switches.VALIDATOR_ADDRESSES.iloc[0]).keys()):
        new_client['generals']['validator'] = loads(state_switches.VALIDATOR_ADDRESSES.iloc[0])[state_client[state_switches.VALIDATOR_SECTION.iloc[0]][state_switches.VALIDATOR_FIELD.iloc[0]]]
    else:
        new_client['generals']['validator'] = loads(state_switches.VALIDATOR_ADDRESSES.iloc[0])['default']

    insert_rows('NCTO', 'ENTERED_CLIENTS', 'KEY, STATUS, CLIENT', [key, 'PENDING'], new_client)

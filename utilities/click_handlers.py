from utilities.queries import insert_rows
from random import randint
from json import loads
from streamlit import cache_resource

def create_new_client(st):
    state_client = st.session_state['newclient']
    state_switches = st.session_state['switches']

    office = st.session_state.offices[st.session_state.offices.OFFICENAME == state_client['general'][-1]['general_office']].OFFICEINDEX.iloc[0]

    if state_client['general'][-1]['general_type'] == 'New Client Relationship':
        originator = int(st.session_state.staff[st.session_state.staff.EMPLOYEE == state_client['general'][-1]['general_originator']].STAFFINDEX.iloc[0])
        max_office_code = st.session_state.clients[st.session_state.clients.OFFICE == state_client['general'][-1]['general_office']].PARENT.astype(int).max()
        client_code = str(max_office_code + 1).zfill(5) + '-000'
        contact_code = str(max_office_code + 2).zfill(5) + '-000'
    else:
        relationship_code = state_client['general'][-1]['general_relationship'][-10:-5]
        parent_client = st.session_state.clients[st.session_state.clients.PARENT == relationship_code]
        max_child = parent_client.CHILD.astype(int).max()
        client_code = relationship_code + '-' + str(max_child + 1).zfill(3)
        originator = int(parent_client.CLIENT_ORIGINATOR_INDEX.iloc[0])
        if state_client['contact'][-1]['contact_index'] == 0:
            contact_code = relationship_code + '-' + str(max_child + 2).zfill(3)
        else:
            contact_code = st.session_state.contacts[st.session_state.contacts.CONTINDEX == state_client['contact'][-1]['contact_index']].CONTCODE.iloc[0]

    key = str(office) + state_client['general'][-1]['general_client'][:3] + str(randint(0, 999999))
    key = key.replace(' ', '_')

    new_client = {'generals': {}, 'client': {}, 'contact': {}, 'billings': {}, 'services': []}

    new_client['generals']['entry'] = state_client['general'][-1]['general_type']
    new_client['generals']['office'] = state_client['general'][-1]['general_office']
    new_client['generals']['client'] = state_client['general'][-1]['general_client']
    new_client['generals']['originator'] = originator
    new_client['generals']['client_code'] = client_code
    new_client['generals']['submitter'] = 'jeremyshank@bmss.com' if st.experimental_user.email == None else st.experimental_user.email
    if state_client[state_switches.VALIDATOR_SECTION.iloc[0]][-1][state_switches.VALIDATOR_FIELD.iloc[0]] in list(loads(state_switches.VALIDATOR_ADDRESSES.iloc[0]).keys()):
        new_client['generals']['validator'] = loads(state_switches.VALIDATOR_ADDRESSES.iloc[0])[state_client[state_switches.VALIDATOR_SECTION.iloc[0]][-1][state_switches.VALIDATOR_FIELD.iloc[0]]]
    else:
        new_client['generals']['validator'] = loads(state_switches.VALIDATOR_ADDRESSES.iloc[0])['default']

    new_client['client']['partner'] = int(st.session_state.staff[st.session_state.staff.EMPLOYEE == state_client['client'][-1]['client_partner']].STAFFINDEX.iloc[0])
    new_client['client']['manager'] = int(st.session_state.staff[st.session_state.staff.EMPLOYEE == state_client['client'][-1]['client_manager']].STAFFINDEX.iloc[0])
    new_client['client']['entity'] = st.session_state.entities[st.session_state.entities.ENTITYNAME == state_client['client'][-1]['client_entity']].ENTITYINDEX.iloc[0]
    new_client['client']['entity_name'] = state_client['client'][-1]['client_entity']
    new_client['client']['industry'] = st.session_state.industries[st.session_state.industries.INDUSTRY == state_client['client'][-1]['client_industry']].INDUSTRYINDEX.iloc[0]
    new_client['client']['address'] = state_client['client'][-1]['client_address']
    new_client['client']['city'] = state_client['client'][-1]['client_city']
    new_client['client']['state'] = state_client['client'][-1]['client_state'] if state_client['client'][-1]['client_country'] == 'United States' else ''
    new_client['client']['province'] = state_client['client'][-1]['client_province'] if state_client['client'][-1]['client_country'] != 'United States' else ''
    new_client['client']['zip'] = state_client['client'][-1]['client_zip']
    new_client['client']['country'] = state_client['client'][-1]['client_country']

    new_client['contact']['first'] = state_client['contact'][-1]['contact_first']
    new_client['contact']['last'] = state_client['contact'][-1]['contact_last']
    new_client['contact']['index'] = int(state_client['contact'][-1]['contact_index'])
    new_client['contact']['email'] = state_client['contact'][-1]['contact_email']
    new_client['contact']['phone'] = state_client['contact'][-1]['contact_phone']
    new_client['contact']['address'] = state_client['contact'][-1]['contact_address']
    new_client['contact']['city'] = state_client['contact'][-1]['contact_city']
    new_client['contact']['state'] = state_client['contact'][-1]['contact_state'] if state_client['contact'][-1]['contact_state'] else ''
    new_client['contact']['province'] = state_client['contact'][-1]['contact_zip'] if state_client['contact'][-1]['contact_zip'] else ''
    new_client['contact']['zip'] = state_client['contact'][-1]['contact_zip']
    new_client['contact']['country'] = state_client['contact'][-1]['contact_country']
    new_client['contact']['code'] = contact_code

    new_client['billings']['fye'] = state_client['billings'][-1]['billings_fye'].strftime('%Y-%m-%d')
    new_client['billings']['invoice'] = 1 if state_client['billings'][-1]['billings_invoice'] == 'Email' else 0
    new_client['billings']['email'] = state_client['billings'][-1]['billings_email']

    service_names = [i for i in state_client['attributes'][-1]['attributes_service']]
    for service in service_names:
        service_index = st.session_state.services[st.session_state.services['SERVTITLE'] == service].SERVINDEX.iloc[0]

        service_entry = [entry for index, entry in enumerate(state_client['services']) if f'services_{service_index}_same' in entry]
        new_client['services'].append({'partner': int(st.session_state.staff[st.session_state.staff.EMPLOYEE == service_entry[-1][f'services_{service_index}_partner']].STAFFINDEX.iloc[0]), 'manager': int(st.session_state.staff[st.session_state.staff.EMPLOYEE == service_entry[-1][f'services_{service_index}_manager']].STAFFINDEX.iloc[0]), 'index': service_index, 'service': service})

    # for key in new_client:
    #     inner_dict = new_client[key]
    #     for inner_key in inner_dict:
    #         if type(inner_dict[inner_key]) != list:
    #             value = inner_dict[inner_key]
    #             value_type = type(value).__name__
    #             st.write(f"{key}.{inner_key}: {value_type}")
    #         else:
    #             for list_dict in inner_dict:
    #                 for list_key in list_dict:
    #                     value = list_dict[list_key]
    #                     value_type = type(value).__name__
    #                     st.write(f"{key}.{inner_key}: {value_type}")


    insert_rows('NCTO', 'ENTERED_CLIENTS', 'KEY, STATUS, CLIENT', [key, 'PENDING'], new_client)

@cache_resource
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def go_to_top(markdown):
    return markdown('[Top of Page](#hello-reports)')

def fill_request(df, session):
    staff = df['EMPLOYEE']
    session['staff_select'] = [staff]
    # session['review_employee'] = [staff]
    project = df['PROJECT']
    session['project_input'] = project

    session['req_link'] = df['IDX']

def submit_review(session):
    # session = st.session_state

    recipient = session.staff[session.staff['EMPLOYEE'] == session['review_employee']]['STAFFINDEX'].iloc[0]

    insert_rows('people', 'review', 'DATE, SENDER, RECIPIENT, PROJECT, SEE_MORE, SEE_LESS, RATING', [session['today'].strftime('%Y-%m-%d'), session['user']['STAFFINDEX'].iloc[0], recipient, session['review_project'], session['review_more'], session['review_less'], session['review_rating']])

    session['staff_select'] = [''] + [i for i in session.staff[session.staff['STAFFINDEX'] != session['user']['STAFFINDEX'].iloc[0]].EMPLOYEE]

    session['project_input'] = ''
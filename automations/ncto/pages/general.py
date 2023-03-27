from utilities.validators import validate_dropdown, validate_string
# from utilities.click_handlers import inc_click - want to use to only render warnings after 

def screen(st):
    st.session_state.valid = [False for i in range(4)]
    general = st.session_state.newclient['general']

    if len(st.session_state.newclient['general']) > 0:
        type_select = [general[-1]['general_type']]
        office = [general[-1]['general_office']]
        client = general[-1]['general_client']
        originator = [general[-1]['general_originator']] if type_select == 'New Client Relationship' else ''
        relationship = [general[-1]['general_relationship']] if type_select == 'Subcode Needed for Existing Client' else ''
    else:
        type_select = ('', 'New Client Relationship', 'Subcode Needed for Existing Client')
        office = [''] + [i for i in st.session_state.offices.OFFICENAME]
        client = ''
        originator = [''] + [i for i in st.session_state.staff.EMPLOYEE]
        relationship = [''] + [i for i in st.session_state.clients[st.session_state.clients['STATUS'] != 'LOST'].CLIENTDISPLAY]

    leftCol, rightCol = st.columns(2)

    leftCol.selectbox('New or Existing Client?', type_select, key='general_type')
    st.session_state.valid[0] = validate_dropdown(st.session_state.general_type, [''])

    warnings = st.expander('View warnings')

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select either new or existing client!')

    rightCol.selectbox('Client Office', office, key='general_office')
    st.session_state.valid[1] = validate_dropdown(st.session_state.general_office, [''])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please select an office for this client!')

    leftCol.text_input('Client Name', client, key='general_client', placeholder='Client Name')
    st.session_state.valid[2] = validate_string(st.session_state.general_client, [''])

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please enter a valid name for this client!')
    elif st.session_state.clients[st.session_state.clients['CLIENT'].str.upper() == st.session_state.general_client.upper()].shape[0] > 0:
        st.session_state.valid[2] = False
        with warnings:
            st.warning('A client with this name already exists! - ' + st.session_state.clients[st.session_state.clients['CLIENT'].str.upper() == st.session_state.general_client.upper()].CLIENTDISPLAY.iloc[0])

    if st.session_state.general_type == "New Client Relationship":
        rightCol.selectbox('Originator', originator, key='general_originator')
        st.session_state.valid[3] = validate_dropdown(st.session_state.general_originator, [''])

        if not st.session_state.valid[3]:
            with warnings:
                st.warning('Please select an originator for this client!')

    elif st.session_state.general_type == 'Subcode Needed for Existing Client':
        rightCol.selectbox('Client Relationship', relationship, key='general_relationship')
        st.session_state.valid[3] = validate_dropdown(st.session_state.general_relationship, [''])

        if not st.session_state.valid[3]:
            with warnings:
                st.warning('Please select a client relationship for this client!')
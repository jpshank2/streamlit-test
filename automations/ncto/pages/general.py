from automations.ncto.validators import validate_dropdown, validate_string

def screen(st):
    st.session_state.valid = [False for i in range(4)]

    leftCol, rightCol = st.columns(2)

    leftCol.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type')
    if not st.session_state.valid[0]:
        st.warning('Please select either new or existing client!')
    st.session_state.valid[0] = validate_dropdown(st.session_state.type, [''])

    rightCol.selectbox('Client Office', [''] + [i for i in st.session_state.offices.OFFICENAME], key='office')
    st.session_state.valid[1] = validate_dropdown(st.session_state.office, [''])

    leftCol.text_input('Client Name', 'Client Name', key='client')
    st.session_state.valid[2] = validate_string(st.session_state.client, ['Client Name'])

    if st.session_state.type == "New Client Relationship":
        rightCol.selectbox('Originator', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='originator')
        st.session_state.valid[3] = validate_dropdown(st.session_state.originator, [''])
    elif st.session_state.type == 'Subcode Needed for Existing Client':
        rightCol.selectbox('Client Relationship', [''] + [i for i in st.session_state.clients.CLIENTDISPLAY], key='relationship')
        st.session_state.valid[3] = validate_dropdown(st.session_state.relationship, [''])


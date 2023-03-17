from utilities.validators import validate_dropdown, validate_string
# from utilities.click_handlers import inc_click - want to use to only render warnings after 

def screen(st):
    st.session_state.valid = [False for i in range(4)]
    st.session_state.clicks = [0 for i in range(4)]

    leftCol, rightCol = st.columns(2)

    leftCol.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type')
    st.session_state.valid[0] = validate_dropdown(st.session_state.type, [''])

    warnings = st.expander('View warnings')

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select either new or existing client!')

    rightCol.selectbox('Client Office', [''] + [i for i in st.session_state.offices.OFFICENAME], key='office')
    st.session_state.valid[1] = validate_dropdown(st.session_state.office, [''])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please select an office for this client!')

    leftCol.text_input('Client Name', 'Client Name', key='client')
    st.session_state.valid[2] = validate_string(st.session_state.client, ['Client Name'])

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please enter a valid name for this client!')

    if st.session_state.type == "New Client Relationship":
        rightCol.selectbox('Originator', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='originator')
        st.session_state.valid[3] = validate_dropdown(st.session_state.originator, [''])

        if not st.session_state.valid[3]:
            with warnings:
                st.warning('Please select an originator for this client!')

    elif st.session_state.type == 'Subcode Needed for Existing Client':
        rightCol.selectbox('Client Relationship', [''] + [i for i in st.session_state.clients.CLIENTDISPLAY], key='relationship')
        st.session_state.valid[3] = validate_dropdown(st.session_state.relationship, [''])

        if not st.session_state.valid[3]:
            with warnings:
                st.warning('Please select a client relationship for this client!')
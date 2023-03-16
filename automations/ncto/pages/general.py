from automations.ncto.validators import validate_dropdown

def screen(st):
    state = st.session_state
    state.valid = [False, False, False, False]

    st.write(state.offices[["OFFICENAME", "OFFICEINDEX"]])

    st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type')
    state.valid[0] = validate_dropdown(state.type, [''])

    st.selectbox('Client Office', [''] + [i for i in state.offices.OFFICENAME], key='office')
    state.valid[1] = validate_dropdown(state.office, [''])

    st.text_input('Client Name', 'Client Name', key='client')
    state.valid[2] = validate_dropdown(state.client, ['', 'Client Name'])

    if state.type == "New Client Relationship":
        st.selectbox('Originator', [''] + [i for i in state.staff.EMPLOYEE], key='originator')
        state.valid[3] = validate_dropdown(state.originator, [''])
    else:
        st.selectbox('Client Relationship', [''] + [i for i in state.clients.CLIENTDISPLAY], key='relationship')
        state.valid[3] = validate_dropdown(state.relationship, [''])


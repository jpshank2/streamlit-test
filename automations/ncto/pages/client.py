from automations.ncto.validators import validate_dropdown, validate_string

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    st.write(st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True])

    st.selectbox('Client Partner', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='clientpartner')
    st.session_state.valid[0] = validate_dropdown(st.session_state.clientpartner, [''])

    # st.selectbox('Client Office', [''] + [i for i in st.session_state.offices.OFFICENAME], key='office')
    # st.session_state.valid[1] = validate_dropdown(st.session_state.office, [''])

    # st.text_input('Client Name', 'Client Name', key='client')
    # st.session_state.valid[2] = validate_string(st.session_state.client, ['Client Name'])

    # if st.session_state.type == "New Client Relationship":
    #     st.selectbox('Originator', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='originator')
    #     st.session_state.valid[3] = validate_dropdown(st.session_state.originator, [''])
    # else:
    #     st.selectbox('Client Relationship', [''] + [i for i in st.session_state.clients.CLIENTDISPLAY], key='relationship')
    #     st.session_state.valid[3] = validate_dropdown(st.session_state.relationship, [''])

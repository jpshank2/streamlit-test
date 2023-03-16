from utilities.queries import run_query
from automations.ncto.validators import validate_dropdown

def screen(st, conn):
    state = st.session_state
    state.valid = [False, False, False, False]

    offices = run_query('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;', conn)
    st.write(offices[["OFFICENAME", "OFFICEINDEX"]])

    st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type')
    state.valid[0] = validate_dropdown(state.type, [''])

    st.selectbox('Client Office', [''] + [i for i in offices.OFFICENAME], key='office')
    state.valid[1] = validate_dropdown(state.office, [''])

    st.text_input('Client Name', 'Client Name', key='client')
    state.valid[2] = validate_dropdown(state.client, ['', 'Client Name'])

    if state.type == "New Client Relationship":
        originators = run_query("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'ACTIVE' AND DEPARTMENT <> 'No Selection';", conn)
        st.selectbox('Originator', [''] + [i for i in originators.EMPLOYEE], key='originator')
        state.valid[3] = validate_dropdown(state.originator, [''])
    else:
        clients = run_query("SELECT * FROM DIM_CLIENT_MASTER WHERE STATUS <> 'LOST';", conn)
        st.selectbox('Client Relationship', [''] + [i for i in clients.CLIENTDISPLAY], key='relationship')
        state.valid[3] = validate_dropdown(state.relationship, [''])


    st.markdown(state)

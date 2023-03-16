from utilities.queries import run_query
from automations.ncto.validators import validate_dropdown

def screen(st, conn):
    #st.session_state.valid = [False, False, False, False]

    offices = run_query('SELECT * FROM DIM_OFFICES WHERE OFFICEINDEX BETWEEN 1 AND 4;', conn)
    st.write(offices[["OFFICENAME", "OFFICEINDEX"]])

    type_select = st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type')
    office_select = st.selectbox('Client Office', [''] + [i for i in offices.OFFICENAME], key='office')
    client_input = st.text_input('Client Name', 'Client Name', key='client')

    if type_select == "New Client Relationship":
        originators = run_query("SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_STATUS = 'ACTIVE' AND DEPARTMENT <> 'No Selection';", conn)
        originator_select = st.selectbox('Originator', [''] + [i for i in originators.EMPLOYEE], key='originator')
    else:
        clients = run_query("SELECT * FROM DIM_CLIENT_MASTER WHERE STATUS <> 'LOST';", conn)
        relationship_select = st.selectbox('Client Relationship', [''] + [i for i in clients.CLIENTDISPLAY], key='relationship')

    st.markdown(st.session_state)

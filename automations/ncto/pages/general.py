from utilities.queries import run_query
from automations.ncto.validators import validate_dropdown

def screen(st, conn):
    offices = run_query('SELECT * FROM DIM_OFFICES;-- WHERE OFFICEINDEX BETWEEN 1 AND 4;', conn)
    st.write(offices[["OFFICENAME", "OFFICEINDEX"]])
    st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'))
    office_select = st.selectbox('Client Office', [i for i in offices.OFFICENAME])

    st.markdown(office_select)

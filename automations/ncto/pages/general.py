import utilities.queries as q

def screen(st, conn):
    offices = q.run_query('SELECT * FROM DIM_OFFICES;', conn)
    st.write(offices[["OFFICENAME", "OFFICEINDEX"]])
    st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'))
    office_select = st.selectbox('Client Office', [i for i in offices.OFFICENAME])

    st.markdown(office_select)

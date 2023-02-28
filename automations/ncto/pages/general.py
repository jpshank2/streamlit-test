import utilities.queries as q

def screen(st, conn):
    offices = q.run_query('SELECT * FROM DIM_OFFICES;', conn)
    st.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'))
    st.selectbox('Client Office', [i for i in offices.OFFICENAME])

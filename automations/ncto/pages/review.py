def screen(st):
    general = st.session_state['newclient']['general'][-1]
    client = st.session_state['newclient']['client'][-1]
    billings = st.session_state['newclient']['billings'][-1]
    contact = st.session_state['newclient']['contact'][-1]
    attributes = st.session_state['newclient']['attributes'][-1]
    allServices = st.session_state['newclient']['services']

    topOne, topTwo, topThree, topFour, topFive, topSix, topSeven = st.columns(7)
    midOne, midTwo, midThree, midFour = st.columns(4)
    botOne, botTwo, botThree = st.columns(3)

    with topOne.container():
        st.markdown(general['general_client'])
        st.caption('Client Name')

    topTwo.markdown(general['general_office'])
    topTwo.caption('Client Office')

    topThree.markdown(client['client_partner'])
    topThree.caption('Client Partner')

    topFour.markdown(client['client_manager'])
    topFour.caption('Client Manager')

    topFive.markdown(general['general_originator']) if general['general_type'] == 'New Client Relationship' else topFive.markdown(general['general_relationship'])
    topFive.caption('Client Originator') if general['general_type'] == 'New Client Relationship' else topFive.caption('Client Relationship')

    topSix.markdown(client['client_entity'])
    topSix.caption('Client Entity')

    topSeven.markdown(client['client_industry'])
    topSeven.caption('Client Industry')
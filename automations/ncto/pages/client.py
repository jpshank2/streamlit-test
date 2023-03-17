from utilities.validators import validate_dropdown, validate_string, validate_nums

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    topLeft, topRight = st.columns(2)

    warnings = st.expander('View warnings')

    topLeft.selectbox('Client Partner', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True].EMPLOYEE], key='clientpartner')
    st.session_state.valid[0] = validate_dropdown(st.session_state.clientpartner, [''])

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select a client partner for this client!')

    topRight.selectbox('Client Manager', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFMANAGER'] == True].EMPLOYEE], key='clientmanager')
    st.session_state.valid[1] = validate_dropdown(st.session_state.clientmanager, [''])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please select a client manager for this client!')
    
    topLeft.selectbox('Client Entity', [''] + [i for i in st.session_state.entities.ENTITYNAME], key='entity')
    st.session_state.valid[2] = validate_dropdown(st.session_state.entity, ['', 'Unknown'])

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please select an entity type for this client!')
    
    topRight.selectbox('Client Industry', [''] + [i for i in st.session_state.industries.INDUSTRY], key='industry')
    st.session_state.valid[3] = validate_dropdown(st.session_state.industry, ['', 'Unknown'])

    if not st.session_state.valid[3]:
        with warnings:
            st.warning('Please select an industry for this client!')

    st.text_input('Client Address', 'Client Address', key='clientaddress')
    st.session_state.valid[4] = validate_string(st.session_state.clientaddress, ['Client Address'])

    if not st.session_state.valid[4]:
        with warnings:
            st.warning('Please enter a valid address for this client!')

    bottomFirst, bottomSecond, bottomThird, bottomFourth = st.columns(4)

    bottomFourth.text_input('Client Country', 'United States', key='clientcountry')
    st.session_state.valid[8] = validate_string(st.session_state.clientcountry, ['', 'US', 'USA', 'United States of America'])

    if not st.session_state.valid[8]:
        with warnings:
            st.warning("Please enter a vaild country for this client! (For US clients please only use 'United States')")

    bottomFirst.text_input('Client City', 'Client City', key='clientcity')
    st.session_state.valid[5] = validate_string(st.session_state.clientcity, ['Client City'])

    if not st.session_state.valid[5]:
        with warnings:
            st.warning('Please enter a valid city for this client!')

    if st.session_state.clientcountry == 'United States':
        bottomSecond.selectbox('Client State', ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"], key='clientstate')
        st.session_state.valid[6] = validate_dropdown(st.session_state.clientstate, [''])

        if not st.session_state.valid[6]:
            with warnings:
                st.warning('Please select a state for this client!')
    else:
        st.text_input('Client Province', 'Client Province', key='clientprovince')
        bottomSecond.session_state.valid[6] = validate_string(st.session_state.clientprovince, ['Client Province'])

        if not st.session_state.valid[6]:
            with warnings:
                st.warning('Please enter a valid province for this client!')

    bottomThird.text_input('Client Zip Code', 'Client Zip', key='clientzip')
    st.session_state.valid[7] = validate_nums(st.session_state.clientzip, 10000, 99999)

    if not st.session_state.valid[7]:
        with warnings:
            st.warning('Please enter a valid zip code for this client! (5 digits, numbers only)')


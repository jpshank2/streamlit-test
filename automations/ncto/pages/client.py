from utilities.validators import validate_dropdown, validate_string, validate_nums

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    topOne, topTwo = st.columns(2)

    st.text_input('Client Address', placeholder='Client Street', key='client_address')
    st.session_state.valid[4] = validate_string(st.session_state.client_address, ['Client Street'])

    bottomOne, bottomTwo, bottomThree, bottomFour = st.columns(4)

    warnings = st.expander('View warnings')

    topOne.selectbox('Client Partner', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True].EMPLOYEE], key='client_partner')
    st.session_state.valid[0] = validate_dropdown(st.session_state.client_partner, [''])

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select a client partner for this client!')

    topTwo.selectbox('Client Manager', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFMANAGER'] == True].EMPLOYEE], key='client_manager')
    st.session_state.valid[1] = validate_dropdown(st.session_state.client_manager, [''])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please select a client manager for this client!')
    
    topOne.selectbox('Client Entity', [''] + [i for i in st.session_state.entities.ENTITYNAME], key='client_entity')
    st.session_state.valid[2] = validate_dropdown(st.session_state.client_entity, ['', 'Unknown'])

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please select an entity type for this client!')
    
    if st.session_state.client_entity == 'INDIVIDUAL':
        indSelect = ['Individual']
        indDisable = True
    else:
        indSelect = [''] + [i for i in st.session_state.industries[st.session_state.industries['INDUSTRY'] != 'Individual'].INDUSTRY]
        indDisable = False
    topTwo.selectbox('Client Industry', indSelect, key='client_industry', disabled=indDisable)
    st.session_state.valid[3] = validate_dropdown(st.session_state.client_industry, ['', 'Unknown', 'No Selection'])

    if not st.session_state.valid[3]:
        with warnings:
            st.warning('Please select an industry for this client!')

    if not st.session_state.valid[4]:
        with warnings:
            st.warning('Please enter a valid address for this client!')

    bottomFour.text_input('Client Country', 'United States', key='client_country', placeholder='Client Country')
    st.session_state.valid[8] = validate_string(st.session_state.client_country, ['US', 'USA', 'United States of America'])

    if not st.session_state.valid[8]:
        with warnings:
            st.warning("Please enter a vaild country for this client! (For US clients please only use 'United States')")

    bottomOne.text_input('Client City', placeholder='Client City', key='client_city')
    st.session_state.valid[5] = validate_string(st.session_state.client_city, ['Client City'])

    if not st.session_state.valid[5]:
        with warnings:
            st.warning('Please enter a valid city for this client!')

    if st.session_state.client_country == 'United States':
        bottomTwo.selectbox('Client State', ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"], key='client_state')
        st.session_state.valid[6] = validate_dropdown(st.session_state.client_state, [''])

        if not st.session_state.valid[6]:
            with warnings:
                st.warning('Please select a state for this client!')
    else:
        bottomTwo.text_input('Client Province', placeholder='Client Province', key='client_province')
        st.session_state.valid[6] = validate_string(st.session_state.client_province, ['Client Province'])

        if not st.session_state.valid[6]:
            with warnings:
                st.warning('Please enter a valid province for this client!')

    bottomThree.text_input('Client Zip Code', placeholder='Numbers Only', key='client_zip')
    st.session_state.valid[7] = validate_nums(st.session_state.client_zip, 10000, 99999)

    if not st.session_state.valid[7]:
        with warnings:
            st.warning('Please enter a valid zip code for this client! (5 digits, numbers only)')


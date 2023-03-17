from utilities.validators import validate_dropdown, validate_string, validate_nums

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    topLeft, topRight = st.columns(2)

    topLeft.selectbox('Client Partner', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True].EMPLOYEE], key='clientpartner')
    st.session_state.valid[0] = validate_dropdown(st.session_state.clientpartner, [''])

    topRight.selectbox('Client Manager', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFMANAGER'] == True].EMPLOYEE], key='clientmanager')
    st.session_state.valid[1] = validate_dropdown(st.session_state.clientmanager, [''])
    
    topLeft.selectbox('Client Entity', [''] + [i for i in st.session_state.entities.ENTITYNAME], key='entity')
    st.session_state.valid[2] = validate_dropdown(st.session_state.entity, ['', 'Unknown'])
    
    topRight.selectbox('Client Industry', [''] + [i for i in st.session_state.industries.INDUSTRY], key='industry')
    st.session_state.valid[3] = validate_dropdown(st.session_state.industry, ['', 'Unknown'])

    st.text_input('Client Address', 'Client Address', key='clientaddress')
    st.session_state.valid[4] = validate_string(st.session_state.clientaddress, ['Client Address'])

    bottomFirst, bottomSecond, bottomThird, bottomFourth = st.columns(4)

    bottomFourth.text_input('Client Country', 'United States', key='clientcountry')
    st.session_state.valid[8] = validate_string(st.session_state.clientcountry, [''])

    bottomFirst.text_input('Client City', 'Client City', key='clientcity')
    st.session_state.valid[5] = validate_string(st.session_state.clientcity, ['Client City'])

    if st.session_state.clientcountry == 'United States':
        bottomSecond.selectbox('Client State', ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"], key='clientstate')
        st.session_state.valid[6] = validate_dropdown(st.session_state.clientstate, [''])
    else:
        st.text_input('Client Province', 'Client Province', key='clientprovince')
        bottomSecond.session_state.valid[6] = validate_string(st.session_state.clientprovince, ['Client Province'])

    bottomThird.text_input('Client Zip Code', 'Client Zip', key='clientzip')
    st.session_state.valid[7] = validate_nums(st.session_state.clientzip, 10000, 99999)


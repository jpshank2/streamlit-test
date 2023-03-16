from automations.ncto.validators import validate_dropdown, validate_string, validate_nums

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    # st.write(st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True])

    st.selectbox('Client Partner', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True].EMPLOYEE], key='clientpartner')
    st.session_state.valid[0] = validate_dropdown(st.session_state.clientpartner, [''])

    st.selectbox('Client Manager', [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFMANAGER'] == True].EMPLOYEE], key='clientmanager')
    st.session_state.valid[1] = validate_dropdown(st.session_state.clientmanager, [''])
    
    st.selectbox('Client Entity', [''] + [i for i in st.session_state.entities.ENTITYNAME], key='entity')
    st.session_state.valid[2] = validate_dropdown(st.session_state.entity, ['', 'Unknown'])
    
    st.selectbox('Client Industry', [''] + [i for i in st.session_state.industries.INDUSTRY], key='industry')
    st.session_state.valid[3] = validate_dropdown(st.session_state.industry, ['', 'Unknown'])

    st.text_input('Client Address', 'Client Address', key='clientaddress')
    st.session_state.valid[4] = validate_string(st.session_state.clientaddress, ['Client Address'])

    st.text_input('Client City', 'Client City', key='clientcity')
    st.session_state.valid[5] = validate_string(st.session_state.clientcity, ['Client City'])

    if st.session_state.clientcountry == 'United States':
        st.selectbox('Client State', ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"], key='clientstate')
        st.session_state.valid[6] = validate_dropdown(st.session_state.clientstate, [''])
    else:
        st.text_input('Client Province', 'Client Province', key='clientprovince')
        st.session_state.valid[6] = validate_string(st.session_state.clientprovince, ['Client Province'])

    st.text_input('Client Zip Code', 'Client Zip', key='clientzip')
    st.session_state.valid[7] = validate_nums(st.session_state.clientzip, 10000, 99999)

    st.text_input('Client Country', 'Client Country', key='clientcountry')
    st.session_state.valid[8] = validate_string(st.session_state.clientcountry, [''])
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


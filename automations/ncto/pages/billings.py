from utilities.validators import validate_dropdown, validate_string, validate_nums, validate_email


def screen(st):
    st.session_state.valid = [False for i in range(9)]

    topOne, topTwo, topThree = st.columns(3)

    upperMidOne, upperMidTwo = st.columns(2)

    lowerMidOne, lowerMidTwo = st.columns(2)

    bottomOne, bottomTwo, bottomThree, bottomFour = st.columns(4)

    warnings = st.expander('View warnings')

    topOne.text_input('Estimated Fees', 'Numbers Only', key='billings_fees')
    st.session_state.valid[0] = validate_nums(st.session_state.billings_fees, 100, 100000000)

    topTwo.text_input('Estimated Hours', 'Numbers Only', key='billings_hours')
    st.session_state.valid[1] = validate_nums(st.session_state.billings_hours, 1, 100000000)

    from datetime import datetime
    today = datetime.now()

    topThree.date_input('Fiscal Year End', value=datetime(int(today.strftime('%Y')), 12, 31), key='billings_fye')

    upperMidOne.selectbox('Client Invoice Method', ('', 'Print and Mail', 'Email'), key='billings_invoice')
    st.session_state.valid[2] = validate_dropdown(st.session_state.billings_invoice, [''])

    upperMidTwo.text_input('Billing Email', 'Required for Email Invoice', key='billings_email')
    if st.session_state.billings_invoice == 'Email':
        st.session_state.valid[3] = validate_email(st.session_state.billings_email)
    elif st.session_state.billings_email != 'Required for Email Invoice' and st.session_state.billings_email != '':
        st.session_state.valid[3] = validate_email(st.session_state.billings_email)
    else:
        st.session_state.valid[3] = True

    lowerMidOne.checkbox('Client and Billing Address Same?', value='billings_same')

    bottomFour.text_input('Billing Country', st.session_state.newclient['client'][-1]['client_country'] if st.session_state.billings_same else 'United States', key='billings_country', disabled=st.session_state.billings_same)

    if st.session_state.billings_same:
        address = st.session_state.newclient['client'][-1]['client_address']
        city = st.session_state.newclient['client'][-1]['client_city']
        zip = st.session_state.newclient['client'][-1]['client_zip']
        if st.session_state.newclient['client'][-1]['client_country'] == 'United States':
            bottomTwo.selectbox('Billing State', st.session_state.newclient['client'][-1]['client_state'], key='billings_state', disabled=st.session_state.billings_same)
        else:
            bottomTwo.text_input('Billing Province', st.session_state.newclient['client'][-1]['client_province'], key='billings_province', disabled=st.session_state.billings_same)
        
        st.session_state.valid[4:9] = [True for j in range(5)]
    else:
        address = 'Billing Street'
        city = 'Billing City'
        zip = 'Numbers Only'
        if st.session_state.billings_country == 'United States':
            bottomTwo.selectbox('Billing State', ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"], key='billings_state', disabled=st.session_state.billings_same)
        else:
            bottomTwo.text_input('Billing Province', 'Billing Province', key='billings_province', disabled=st.session_state.billings_same)

    lowerMidTwo.text_input('Billing Address', address, key='billings_address', disabled=st.session_state.billings_same)

    bottomOne.text_input('Billing City', city, key='billings_city', disabled=st.session_state.billings_same)
    
    bottomThree.text_input('Billing Zip Code', zip, key='billings_zip', disabled=st.session_state.billings_same)

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please enter valid estimated fees for this client!')
    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please enter valid estimated hours for this client!')
    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please select an invoice method for this client!')
    if not st.session_state.valid[3]:
        with warnings:
            st.warning('Please enter a valid billing email for this client!')

    if not st.session_state.billings_same:
        st.session_state.valid[4] = validate_string(st.session_state.billings_address, ['Billing Street'])
        st.session_state.valid[5] = validate_string(st.session_state.billings_city, ['Billing City'])
        st.session_state.valid[6] = validate_dropdown(st.session_state.billings_state, ['']) if st.session_state.billings_country == 'United States' else validate_string(st.session_state.billings_province, ['Billing Province'])
        st.session_state.valid[7] = validate_nums(st.session_state.billings_zip, 10000, 99999)
        st.session_state.valid[8] = validate_string(st.session_state.billings_country, ['US', 'USA', 'United States of America'])

        with warnings:
            if not st.session_state.valid[4]:
                st.warning('Please enter a valid billing address for this client!')
            if not st.session_state.valid[5]:
                st.warning('Please enter a valid billing city for this client!')
            if not st.session_state.valid[6]:
                st.warning('Please select a state for this client!') if st.session_state.billings_country == 'United States' else st.warning('Please enter a valid billing province for this client!')
            if not st.session_state.valid[7]:
                st.warning("Please enter a valid billing zip code for this client! (5 digits, numbers only)")
            if not st.session_state.valid[8]:
                st.warning("Please enter a vaild country for this client! (For US clients please only use 'United States')")

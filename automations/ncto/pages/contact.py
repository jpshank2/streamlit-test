from utilities.validators import validate_dropdown, validate_string, validate_nums, validate_email

def screen(st):
    st.session_state.valid = [False for i in range(9)]

    topOne, topTwo, topThree, topFour = st.columns(4)

    midOne, midTwo = st.columns(2)

    bottomOne, bottomTwo, bottomThree, bottomFour = st.columns(4)

    warnings = st.expander('View warnings')

    topOne.text_input('First Name', 'First Name', key='contact_first')
    st.session_state.valid[0] = validate_string(st.session_state.contact_first, ['First Name'])

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please enter a valid first name for this contact!')

    topTwo.text_input('Last Name', 'Last Name', key='contact_last')
    st.session_state.valid[1] = validate_string(st.session_state.contact_last, ['Last Name'])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please enter a valid last name for this contact!')

    topThree.text_input('Contact Email', 'Contact Email', key='contact_email')
    st.session_state.valid[2] = validate_email(st.session_state.contact_email)

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please enter a valid email for this contact!')

    topFour.text_input('Contact Phone Number', 'Numbers Only', key='contact_phone')
    if st.session_state.contact_phone != 'Numbers Only' and st.session_state.contact_phone != '':
        st.session_state.valid[3] = validate_nums(st.session_state.contact_phone, 1000000000, 9999999999)
    else:
        st.session_state.valid[3] = True

    if not st.session_state.valid[3]:
        with warnings:
            st.warning('Please enter a valid phone number for this contact!')

    midOne.checkbox('Client and Contact Address Same?', key='contact_same')

    if st.session_state.contact_same:
        address = st.session_state.newclient['client'][-1]['client_address']
        city = st.session_state.newclient['client'][-1]['client_city']
        country = st.session_state.newclient['client'][-1]['client_country']
        state = st.session_state.newclient['client'][-1]['client_state']
        province = st.session_state.newclient['client'][-1]['client_province']
        zip = st.session_state.newclient['client'][-1]['client_zip']
        
        st.session_state.valid[4:9] = [True for j in range(5)]
    else:
        address = 'Contact Street'
        city = 'Contact City'
        country = 'United States'
        state = ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
        province = 'Contact Province'
        zip = 'Numbers Only'

    midTwo.text_input('Contact Address', address, key='contact_address', disabled=st.session_state.contact_same)

    bottomOne.text_input('Contact City', city, key='contact_city', disabled=st.session_state.contact_same)

    bottomFour.text_input('Contact Country', country, key='contact_country')
    # st.session_state.valid[8] = validate_string(st.session_state.clientcountry, ['US', 'USA', 'United States of America'])
    if st.session_state.contact_country == 'United States':
        bottomTwo.selectbox('Contact State', state, key='contact_state', disabled=st.session_state.contact_same)
    else:
        bottomTwo.text_input('Contact Province', province, key='contact_province', disabled=st.session_state.contact_same)
    
    bottomThree.text_input('Contact Zip Code', zip, key='contact_zip')

    if not st.session_state.contact_same:
        st.session_state.valid[4] = validate_string(st.session_state.contact_address, ['Contact Street'])
        st.session_state.valid[5] = validate_string(st.session_state.contact_city, ['Contact City'])
        st.session_state.valid[6] = validate_dropdown(st.session_state.contact_state, ['']) if st.session_state.contact_country == 'United States' else validate_string(st.session_state.contact_province, ['Contact Province'])
        st.session_state.valid[7] = validate_nums(st.session_state.contact_zip, 10000, 99999)
        st.session_state.valid[8] = validate_string(st.session_state.contact_country, ['US', 'USA', 'United States of America'])

        with warnings:
            if not st.session_state.valid[4]:
                st.warning('Please enter a valid address for this contact!')
            if not st.session_state.valid[5]:
                st.warning('Please enter a valid city for this contact!')
            if not st.session_state.valid[6]:
                st.warning('Please select a state for this contact!') if st.session_state.contact_country == 'United States' else st.warning('Please enter a valid province for this contact!')
            if not st.session_state.valid[7]:
                st.warning("Please enter a valid zip code for this contact! (5 digits, numbers only)")
            if not st.session_state.valid[8]:
                st.warning("Please enter a vaild country for this contact! (For US clients please only use 'United States')")


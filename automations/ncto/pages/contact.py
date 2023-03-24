from utilities.validators import validate_dropdown, validate_string, validate_nums, validate_email

def screen(st):
    st.session_state.valid = [False for i in range(9)]
    
    address = 'Contact Street'
    city = 'Contact City'
    zip = 'Numbers Only'
    first = 'First Name'
    last = 'Last Name'
    email = 'Contact Email'
    state = ["", "AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
    province = 'Contact Province'
    country = 'United States'

    topOne, topTwo, topThree, topFour = st.columns(4)

    midOne, midTwo = st.columns(2)

    bottomOne, bottomTwo, bottomThree, bottomFour = st.columns(4)

    contactButtonOne, contactButtonTwo = st.columns(2)

    warnings = st.expander('View warnings')

    contactButtonOne.checkbox('Search for an Existing Contact', key='existing_toggle', value=False)
    contactButtonTwo.selectbox('Select an existing contact', [''] + [i for i in st.session_state.contacts.CONTDISPLAY], key='existing_contact', disabled=(not st.session_state.existing_toggle))

    midOne.checkbox('Client and Contact Address Same?', key='contact_same', disabled=st.session_state.existing_toggle)
    if st.session_state.existing_toggle:
        contact = st.session_state.contacts[st.session_state.contacts.CONTDISPLAY == st.session_state.existing_contact]
        if validate_dropdown(st.session_state.existing_contact, ['']):
            st.session_state.valid = [True for i in range(10)]
            name = contact['CONTNAME'].iloc[0].split(' ', maxsplit=1)
            address = contact['CONTADDRESS'].iloc[0]
            city = contact['CONTCITY'].iloc[0]
            zip = contact['CONTZIP'].iloc[0]
            first = name[0]
            last = name[1]
            email = contact['CONTEMAIL'].iloc[0]
            state = [contact['CONTSTATE'].iloc[0]]
            province = contact['CONTSTATE'].iloc[0]
            country = contact['CONTCOUNTRY'].iloc[0]
            if 'contact_index' not in st.session_state:
                st.session_state['contact_index'] = contact['CONTINDEX'].iloc[0]
            else:
                st.session_state['contact_index'] = contact['CONTINDEX'].iloc[0]
        else:    
            st.session_state.valid = [True for i in range(9)] + [False]
            warnings.warning('Please select a valid existing contact for this client!')
    elif st.session_state.contact_same:
        address = st.session_state.newclient['client'][-1]['client_address']
        city = st.session_state.newclient['client'][-1]['client_city']
        zip = st.session_state.newclient['client'][-1]['client_zip']
        country = st.session_state.newclient['client'][-1]['client_country']
        if country == 'United States':
            state = [st.session_state.newclient['client'][-1]['client_state']]
        else:
            province = st.session_state.newclient['client'][-1]['client_province']
        
        st.session_state.valid[4:9] = [True for j in range(5)]

    # existingContact = st.columns(1)

    topOne.text_input('First Name', first, key='contact_first', disabled=st.session_state.existing_toggle)
    st.session_state.valid[0] = validate_string(st.session_state.contact_first, ['First Name'])

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please enter a valid first name for this contact!')

    topTwo.text_input('Last Name', last, key='contact_last', disabled=st.session_state.existing_toggle)
    st.session_state.valid[1] = validate_string(st.session_state.contact_last, ['Last Name'])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please enter a valid last name for this contact!')

    topThree.text_input('Contact Email', email, key='contact_email', disabled=st.session_state.existing_toggle)
    st.session_state.valid[2] = validate_email(st.session_state.contact_email)

    if not st.session_state.valid[2]:
        with warnings:
            st.warning('Please enter a valid email for this contact!')

    topFour.text_input('Contact Phone Number', 'Numbers Only', key='contact_phone', disabled=st.session_state.existing_toggle)
    if st.session_state.contact_phone != 'Numbers Only' and st.session_state.contact_phone != '':
        st.session_state.valid[3] = validate_nums(st.session_state.contact_phone, 1000000000, 9999999999)
    else:
        st.session_state.valid[3] = True

    if not st.session_state.valid[3]:
        with warnings:
            st.warning('Please enter a valid phone number for this contact! (Numbers only with area code)')


    bottomFour.text_input('Contact Country', country, key='contact_country', disabled=(st.session_state.contact_same or st.session_state.existing_toggle))

    midTwo.text_input('Contact Address', address, key='contact_address', disabled=(st.session_state.contact_same or st.session_state.existing_toggle))

    bottomOne.text_input('Contact City', city, key='contact_city', disabled=(st.session_state.contact_same or st.session_state.existing_toggle))

    bottomTwo.selectbox('Contact State', state, key='contact_state', disabled=(st.session_state.contact_same or st.session_state.existing_toggle)) if st.session_state.contact_country == 'United States' else bottomTwo.text_input('Contact Province', province, key='contact_province', disabled=(st.session_state.contact_same or st.session_state.existing_toggle))
    
    bottomThree.text_input('Contact Zip Code', zip, key='contact_zip', disabled=(st.session_state.contact_same or st.session_state.existing_toggle))

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

    
    if st.session_state.existing_toggle:
        contact = st.session_state.contacts[st.session_state.contacts.CONTDISPLAY == st.session_state.existing_contact]
        if validate_dropdown(st.session_state.existing_contact, ['']):
            # st.session_state.valid = [True for i in range(9)]
            if 'contact_index' not in st.session_state:
                st.session_state['contact_index'] = contact['CONTINDEX'].iloc[0]
            else:
                st.session_state['contact_index'] = contact['CONTINDEX'].iloc[0]
        else:
            st.session_state.valid = [True for i in range(9)] + [False]
            warnings.warning('Please select a valid existing contact for this client!')
    else:
        st.session_state.valid[0] = validate_string(st.session_state.contact_first, ['First Name'])
        st.session_state.valid[1] = validate_string(st.session_state.contact_last, ['Last Name'])
        st.session_state.valid[2] = validate_email(st.session_state.contact_email)
        if st.session_state.contact_phone != 'Numbers Only' and st.session_state.contact_phone != '':
            st.session_state.valid[3] = validate_nums(st.session_state.contact_phone, 1000000000, 9999999999)
        else:
            st.session_state.valid[3] = True
        st.session_state.valid[4] = validate_string(st.session_state.contact_address, ['Contact Street'])
        st.session_state.valid[5] = validate_string(st.session_state.contact_city, ['Contact City'])
        st.session_state.valid[6] = validate_dropdown(st.session_state.contact_state, ['']) if st.session_state.contact_country == 'United States' else validate_string(st.session_state.contact_province, ['Contact Province'])
        st.session_state.valid[7] = validate_nums(st.session_state.contact_zip, 10000, 99999)
        st.session_state.valid[8] = validate_string(st.session_state.contact_country, ['US', 'USA', 'United States of America'])
        if 'contact_index' not in st.session_state:
            st.session_state['contact_index'] = 0
        else:
            st.session_state['contact_index'] = 0
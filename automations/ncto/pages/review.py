def screen(st):
    general = st.session_state['newclient']['general'][-1]
    client = st.session_state['newclient']['client'][-1]
    billings = st.session_state['newclient']['billings'][-1]
    contact = st.session_state['newclient']['contact'][-1]
    attributes = st.session_state['newclient']['attributes'][-1]
    allServices = st.session_state['newclient']['services']

    topOne, topTwo, topThree, topFour = st.columns(4)
    upperMidOne, upperMidTwo, upperMidThree = st.columns(3)
    midOne, midTwo, midThree, midFour = st.columns(4)
    botOne, botTwo, botThree = st.columns(3)

    topOne.caption('Client Name')
    topOne.markdown(general['general_client'])

    topTwo.caption('Client Office')
    topTwo.markdown(general['general_office'])

    topThree.caption('Client Partner')
    topThree.markdown(client['client_partner'])

    topFour.caption('Client Manager')
    topFour.markdown(client['client_manager'])

    upperMidOne.caption('Client Originator') if general['general_type'] == 'New Client Relationship' else upperMidOne.caption('Client Relationship')
    upperMidOne.markdown(general['general_originator']) if general['general_type'] == 'New Client Relationship' else upperMidOne.markdown(general['general_relationship'])

    upperMidTwo.caption('Client Entity')
    upperMidTwo.markdown(client['client_entity'])

    upperMidThree.caption('Client Industry')
    upperMidThree.markdown(client['client_industry'])

    midOne.caption('Contact Address')
    midOne.markdown(contact['contact_address'] + '\n' + contact['contact_city'] + ', ' + contact['contact_state'] if contact['contact_country'] == 'United States' else contact['contact_province'] + ' ' + contact['contact_zip'] + ' ' + contact['contact_country'])

    midTwo.caption('Billing Address')
    midTwo.markdown(billings['billings_address'] + '\n' + billings['billings_city'] + ', ' + billings['billings_state'] if billings['billings_country'] == 'United States' else billings['billings_province'] + ' ' + billings['billings_zip'] + ' ' + billings['billings_country'])

    midThree.caption('Client Address')
    midThree.markdown(client['client_address'] + '\n' + client['client_city'] + ', ' + client['client_state'] if client['client_country'] == 'United States' else client['client_province'] + ' ' + client['client_zip'] + ' ' + client['client_country'])

    midFour.caption('Contact Phone Number')
    midFour.markdown(contact['contact_phone'] if contact['contact_phone'] != 'Numbers Only' and contact['contact_phone'] != '' else 'No phone number listed')

    botOne.caption('Contact Email')
    botOne.markdown(contact['contact_email'])

    botTwo.caption('Client Invoice Method')
    botTwo.markdown(billings['billings_invoice'])

    botThree.text_input('Client Notes', placeholder='Enter Any Additional Notes, Jobs to be added, etc.', key='review_notes')

    service_names = [i for i in attributes['attributes_service']]
    partners = list()
    managers = list()

    for service in service_names:
        service_index = st.session_state.services[st.session_state.services['SERVTITLE'] == service].SERVINDEX.iloc[0]
        partner = f'services_{service_index}_partner'
        manager = f'services_{service_index}_manager'

        service_entry = [entry for index, entry in enumerate(allServices) if partner in entry]
        partners.append(service_entry[-1][partner])
        managers.append(service_entry[-1][manager])


    from pandas import DataFrame
    st.caption('Client Services')
    st.write(DataFrame({'Client Service': service_names, 'Service Partner': partners, 'Service Manager': managers}))

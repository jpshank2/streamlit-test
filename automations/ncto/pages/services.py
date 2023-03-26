from utilities.validators import validate_dropdown

def screen(st, service):
    servIndex = st.session_state.services[st.session_state.services['SERVTITLE'] == service]
    sameKey = 'services_' + servIndex + '_same'
    servicePartner = 'services_' + servIndex + '_partner'
    serviceManager = 'services_' + servIndex + '_manager'
    st.session_state.valid = [False for i in range(2)]

    st.markdown('### ' + service + ' Service Information')
    st.write(st.session_state.services)

    topOne, topTwo = st.columns(2)
    midOne, midTwo = st.columns(2)
    botOne, botTwo = st.columns(2)

    warnings = st.expander('View warnings')

    midTwo.checkbox('Same as Client Partner and Manager?', key=sameKey, value=False)

    if st.session_state[sameKey]:
        partner = [st.session_state.newclient['client'][-1]['client_partner']]
        manager = [st.session_state.newclient['client'][-1]['client_manager']]
    else:
        partner = [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFCLIENTRESPONSIBLE'] == True].EMPLOYEE]
        manager = [''] + [i for i in st.session_state.staff[st.session_state.staff['STAFFMANAGER'] == True].EMPLOYEE]

    topOne.selectbox(service + ' Partner', partner, key=servicePartner, disabled=st.session_state.services_same)
    st.session_state.valid[0] = validate_dropdown(st.session_state.services_partner, [''])

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select a service partner for this client!')

    botOne.selectbox(service + ' Manager', manager, key=serviceManager, disabled=st.session_state.services_same)
    st.session_state.valid[1] = validate_dropdown(st.session_state.services_partner, [''])

    if not st.session_state.valid[1]:
        with warnings:
            st.warning('Please select a service manager for this client!')

    topTwo.empty()
    midOne.empty()
    botTwo.empty()

    st.write(st.session_state['newclient']['attributes'][-1]['attributes_service'])
    st.write(st.session_state.serviceCounter)

    # if st.session_state.newclient['client'][-1]['client_entity'] == 'INDIVIDUAL':
    #     available_servs = st.session_state.services[st.session_state.services['SERVPERSON'] == True]
    # else:
    #     available_servs = st.session_state.services[st.session_state.services['SERVORG'] == True]

    # st.multiselect('Client Services', available_servs.SERVTITLE, key='attributes_service')
    # st.session_state.valid[0] = validate_multi(st.session_state.attributes_service)

    # warnings = st.expander('View warnings')

    # if not st.session_state.valid[0]:
    #     with warnings:
    #         st.warning('Please select at least one service for this client!')
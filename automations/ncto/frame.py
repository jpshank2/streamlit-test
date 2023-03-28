from utilities.click_handlers import create_new_client

def next_page(st, screen):
    prefix = screen + '_'
    allSessions = list(st.session_state.keys())
    sessionsForJSON = [k for k in allSessions if prefix in k]
    JSONtoAdd = dict()
    if screen == 'home':
        st.session_state.pageCounter += 1
    elif screen == 'services':
        # write each service to dict of values
        for session in sessionsForJSON:
            JSONtoAdd[session] = st.session_state[session]

        st.session_state['newclient'][screen].append(JSONtoAdd)
        if st.session_state.serviceCounter < len(st.session_state['newclient']['attributes'][-1]['attributes_service']) - 1:
            st.session_state.serviceCounter += 1
        else:
            st.session_state.pageCounter += 1
    else:
        for session in sessionsForJSON:
            JSONtoAdd[session] = st.session_state[session]

        st.session_state['newclient'][screen].append(JSONtoAdd)

        st.session_state.pageCounter += 1
        
        if screen == 'review':
            create_new_client(st)

def prev_page(st):
    st.session_state.pageCounter -= 1

def reset(st):
    st.session_state.pageCounter = 0
    st.session_state.serviceCounter = 0
    st.session_state.newclient = {'general': [], 'client': [], 'contact': [], 'billings': [], 'attributes': [], 'services': [], 'review': []}

#NCTO function
def clientTakeOn(st):

    try:
        pageList = st.session_state['switches'].NCTO_PAGES.iloc[0].split('}, ')
        st.write(pageList)
    except:
        pageList = [{'name': 'General Information', 'module': 'automations.ncto.pages.general'}, {'name': 'Client Details', 'module': 'automations.ncto.pages.client'}, {'name': 'Contact Details', 'module': 'automations.ncto.pages.contact'}, {'name': 'Client Billings', 'module': 'automations.ncto.pages.billings'}, {'name': 'Client Attributes', 'module': 'automations.ncto.pages.attributes'}, {'name': 'Services', 'module': 'automations.ncto.pages.services'}, {'name': 'Final Review', 'module': 'automations.ncto.pages.review'}, {'name': 'Submitted', 'module': 'automations.ncto.pages.end'}]
    
    # dictionary that can be added to, that can interact with the list of pages that we have up above

    st.markdown('## ' + pageList[st.session_state.pageCounter]['name'])

    try:

        from importlib import import_module
        screen = import_module(pageList[st.session_state.pageCounter]['module'])

        if pageList[st.session_state.pageCounter]['name'] == 'Services':
            if 'serviceCounter' not in st.session_state:
                st.session_state['serviceCounter'] = 0
            screen.screen(st, st.session_state['newclient']['attributes'][-1]['attributes_service'][st.session_state.serviceCounter])
        # elif pageList[st.session_state.pageCounter]['name'] == 'Home':
        #     st.session_state.valid = [True]
        #     screen.screen(st)
        else:
            screen.screen(st)

        leftButton, rightButton = st.columns(2)

        if st.session_state.pageCounter > 0 and st.session_state.pageCounter < len(pageList) - 1:
            leftButton.button('Previous Page', on_click=prev_page, args=(st,), key='previous')

        if pageList[st.session_state.pageCounter]['name'] == 'Submitted':
            rightButton.button('Enter a new client', key='next', on_click=reset, args=(st, ), disabled=(False in st.session_state['valid']))
        else:
            rightButton.button('Save & Next' if pageList[st.session_state.pageCounter]['name'] != 'Final Review' else 'Submit', key='next', on_click=next_page, args=(st, pageList[st.session_state.pageCounter]['module'].split('.')[-1]), disabled=(False in st.session_state['valid']))
    except Exception as e:
        st.write(e)
        st.write(st.session_state.newclient)

    progress_bar = st.progress(0)
    progress_bar.progress(int(100 * (st.session_state.pageCounter / (len(pageList) - 1))))
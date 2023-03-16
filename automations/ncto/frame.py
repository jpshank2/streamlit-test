#move from page to page in the def ClientTakeOn
def next_page(st):
    st.session_state.pageCounter += 1
    
    allSessions = list(st.session_state.keys())
    sessionsToRemove = list(filter(lambda x: all([x != y for y in st.session_state.static_session]), allSessions))

    for session in sessionsToRemove:
        del st.session_state[session]

def prev_page(st):
    st.session_state.pageCounter -= 1

    allSessions = list(st.session_state.keys())
    sessionsToRemove = list(filter(lambda x: all([x != y for y in st.session_state.static_session]), allSessions))

    for session in sessionsToRemove:
        del st.session_state[session]

#NCTO function
def clientTakeOn(st):
    if 'static_session' not in st.session_state:
        st.session_state['static_session'] = ['previous', 'next', 'staff', 'clients', 'offices', 'entities', 'industries', 'valid', 'pageCounter', 'static_session']
    
    pageList = [{'name': 'Home', 'module': 'automations.ncto.pages.home'}, {'name': 'General Information', 'module': 'automations.ncto.pages.general'}, {'name': 'Client Details', 'module': 'automations.ncto.pages.client'}, {'name': 'Contact Details', 'module': 'automations.ncto.pages.contact'}, {'name': 'Client Billings', 'module': 'automations.ncto.pages.billings'}, {'name': 'Client Attributes', 'module': 'automations.ncto.pages.attributes'}, {'name': 'Services', 'module': 'automations.ncto.pages.services'}, {'name': 'Final Review', 'module': 'automations.ncto.pages.review'}, {'name': 'Submitted', 'module': 'automations.ncto.pages.end'}]
    
    # dictionary that can be added to, that can interact with the list of pages that we have up above

    st.markdown('## ' + pageList[st.session_state.pageCounter]['name'])

    st.write(list(st.session_state.keys()))

    from importlib import import_module
    screen = import_module(pageList[st.session_state.pageCounter]['module'])

    if st.session_state.pageCounter == 6:
        screen.screen(st)
    elif st.session_state.pageCounter == 0:
        st.session_state.valid = [True]
        screen.screen(st)
    else:
        screen.screen(st)

    if st.session_state.pageCounter > 0:
        st.button('Previous Page', on_click=prev_page, args=(st,), key='previous')

    st.button('Save & Next', key='next', on_click=next_page, args=(st,), disabled=(False in st.session_state['valid']))

    progress_bar = st.progress(0)
    progress_bar.progress(int(100 * (st.session_state.pageCounter / len(pageList))))
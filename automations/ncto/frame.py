def next_page(st):
    st.session_state.pageCounter += 1

def prev_page(st):
    st.session_state.pageCounter -= 1

def clientTakeOn(st, conn):
    pageList = [{'name': 'Main', 'module': 'automations.ncto.pages.home'}, {'name': 'General Information', 'module': 'automations.ncto.pages.general'}, {'name': 'Client Details', 'module': 'automations.ncto.pages.client'}, {'name': 'Contact Details', 'module': 'automations.ncto.pages.contact'}, {'name': 'Client Billings', 'module': 'automations.ncto.pages.billings'}, {'name': 'Client Attributes', 'module': 'automations.ncto.pages.attributes'}, {'name': 'Services', 'module': 'automations.ncto.pages.services'}, {'name': 'Final Review', 'module': 'automations.ncto.pages.review'}, {'name': 'Submitted', 'module': 'automations.ncto.pages.end'}]
    
    if 'pageCounter' not in st.session_state:
        st.session_state['pageCounter'] = 0

    st.markdown('## ' + pageList[st.session_state.pageCounter]['name'])

    from importlib import import_module
    screen = import_module(pageList[st.session_state.pageCounter]['module'])

    services = list()

    if st.session_state.pageCounter == 0:
        display = screen.screen(st)
    elif pageList[st.session_state.pageCounter]['name'] == 'Services':
        display = screen.screen(st, conn, services)
    else:
        display = screen.screen(st, conn)

    if st.session_state.pageCounter > 0:
        st.button('Previous Page', on_click=prev_page, args=(st,))

    st.button('Save & Next', key=(f'button-{st.session_state.pageCounter}'), on_click=next_page, args=(st,))

    progress_bar = st.progress(0)
    progress_bar.progress(int(100 * (st.session_state.pageCounter / len(pageList))))
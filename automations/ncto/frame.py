def next_page(page):
    return page + 1

def clientTakeOn(st):
    pageList = [{'name': 'Home', 'module': 'automations.ncto.pages.home'}, {'name': 'General Information', 'module': 'automations.ncto.pages.general'}, {'name': 'Client Details', 'module': 'automations.ncto.pages.client'}, {'name': 'Contact Details', 'module': 'automations.ncto.pages.contact'}, {'name': 'Client Billings', 'module': 'automations.ncto.pages.billings'}, {'name': 'Client Attributes', 'module': 'automations.ncto.pages.attributes'}, {'name': 'Services', 'module': 'automations.ncto.pages.services'}, {'name': 'Final Review', 'module': 'automations.ncto.pages.review'}, {'name': 'Submitted', 'module': 'automations.ncto.pages.end'}]

    pageCounter = 0

    st.write(pageList[pageCounter])
    from importlib import import_module
    screen = import_module(pageList[pageCounter]['module'])

    if pageCounter == 6:
        screen.screen(st, )

    screen.screen(st)

    st.button('Save & Next', on_click=next_page, args=(pageCounter,))
def clientTakeOn(st):
    pageList = [{'name': 'Home', 'module': 'pages.home'}, {'name': 'General Information', 'module': 'pages.general'}, {'name': 'Client Details', 'module': 'pages.client'}, {'name': 'Contact Details', 'module': 'pages.contact'}, {'name': 'Client Billings', 'module': 'pages.billings'}, {'name': 'Client Attributes', 'module': 'pages.attributes'}, {'name': 'Services', 'module': 'pages.services'}, {'name': 'Final Review', 'module': 'pages.review'}, {'name': 'Submitted', 'module': 'pages.end'}]

    pageCounter = 0

    while True:
        st.write(pageList[pageCounter])
        from importlib import import_module
        screen = import_module(pageList[pageCounter]['module'])

        screen.screen(st)
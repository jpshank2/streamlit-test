def next_page(st):
    st.session_state.pageCounter += 1

def clientTakeOn(st):
    pageList = [{'name': 'Home', 'module': 'automations.ncto.pages.home'}, {'name': 'General Information', 'module': 'automations.ncto.pages.general'}, {'name': 'Client Details', 'module': 'automations.ncto.pages.client'}, {'name': 'Contact Details', 'module': 'automations.ncto.pages.contact'}, {'name': 'Client Billings', 'module': 'automations.ncto.pages.billings'}, {'name': 'Client Attributes', 'module': 'automations.ncto.pages.attributes'}, {'name': 'Services', 'module': 'automations.ncto.pages.services'}, {'name': 'Final Review', 'module': 'automations.ncto.pages.review'}, {'name': 'Submitted', 'module': 'automations.ncto.pages.end'}]
    if 'pageCounter' not in st.session_state:
        st.session_state['pageCounter'] = 0

    st.write(pageList[st.session_state.pageCounter])
    from importlib import import_module
    screen = import_module(pageList[st.session_state.pageCounter]['module'])

    while True:
        if st.session_state.pageCounter == 6:
            screen.screen(st, )

        screen.screen(st)

        st.button('Save & Next', on_click=next_page, args=(st,))

    # while True:    
    #     num = st.session_state.num

    #     if placeholder2.button('end', key=num):
    #         placeholder2.empty()
    #         df = pd.DataFrame(st.session_state.data)
    #         st.dataframe(df)
    #         break
    #     else:        
    #         with placeholder.form(key=str(num)):
    #             new_student = NewStudent(page_id=num)        

    #             if st.form_submit_button('register'):                
    #                 st.session_state.data.append({
    #                     'id': num, 'name': new_student.name, 'age': new_student.age})
    #                 st.session_state.num += 1
    #                 placeholder.empty()
    #                 placeholder2.empty()
    #             else:
    #                 st.stop()
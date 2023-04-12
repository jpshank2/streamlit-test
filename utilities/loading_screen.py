from utilities.queries import validation_company, get_rows, init_connection

def loading(st):
    # if st.experimental_user.email == 'jpshank2@gmail.com':
    #     email = 'jeremyshank@bmss.com'
    if st.experimental_user.email == 'jdavidbrowncpa@gmail.com':
        email = 'dbrown@bmss.com'
    elif st.experimental_user.email == 'imesser@abacustechnologies.com':
        email = 'kfluker@bmss.com'
    else:
        email = 'ar@bmss.com'#st.experimental_user.email
        
    domain = email.split('@')[-1]

    with st.spinner('Curating your experience...'):
        company = validation_company(domain)
        if company.empty:
            st.markdown("We're sorry, you are not a registered company with Magnify")
            st.markdown("Please [email us](mailto:bizintel@abacustechnologies.com?subject=Magnify) to join the Magnify community")
        else:
            if 'company' not in st.session_state:
                st.session_state['company'] = company
            if 'conn' not in st.session_state:
                st.session_state['conn'] = init_connection()
            if 'user' not in st.session_state:
                st.session_state['user'] = get_rows(f"SELECT S.*, L.LEVEL_PERMISSION FROM DIM_STAFF_MASTER S INNER JOIN CONFIGURATIONS.LEVELS L ON L.LEVEL_DESC = S.LEVEL WHERE STAFF_EMAIL = '{email}'")
            if 'level' not in st.session_state:
                st.session_state['level'] = st.session_state['user'].LEVEL.iloc[0]
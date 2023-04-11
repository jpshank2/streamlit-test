from utilities.queries import validation_connection, get_rows, init_connection
def loading(st):
    email = 'jeremyshank@bmss.com' if st.experimental_user.email == 'jpshank2@gmail.com' else st.experimental_user.email
    domain = email.split('@')[-1]
    st.write(email)
    st.write(domain)

    with st.spinner('Curating your experience...'):
        conn = validation_connection()
        company = get_rows(f"SELECT * FROM COMPANIES WHERE DOMAIN = '{domain}'", conn)
        if company.empty:
            st.markdown("We're sorry, you are not a registered company with Magnify")
            st.markdown("Please [contact us](mailto:bizintel@abacustechnologies.com?subject=Join Magnify) to join the Magnify community")
        else:
            st.markdown('Welcome to Magnify!')
            if 'company' not in st.session_state:
                st.session_state['company'] = company
            if 'conn' not in st.session_state:
                st.session_state['conn'] = init_connection()
            if 'user' not in st.session_state:
                st.session_state['user'] = get_rows(f"SELECT * FROM DIM_STAFF_MASTER WHERE STAFF_EMAIL = '{email}'")

            conn.close()
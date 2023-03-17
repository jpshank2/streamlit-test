from utilities.validators import validate_dropdown, validate_string
# from utilities.click_handlers import inc_click

def screen(st):

    def inc_click(position):
        updatedClicks = st.session_state.clicks
        updatedClicks[position] = updatedClicks[position] + 1
        st.session_state.clicks = updatedClicks

    st.session_state.valid = [False for i in range(4)]
    st.session_state.clicks = [0 for i in range(4)]

    leftCol, rightCol = st.columns(2)

    leftCol.selectbox('New or Existing Client?', ('', 'New Client Relationship', 'Subcode Needed for Existing Client'), key='type', on_change=(lambda: st.session_state.clicks[0] + 1))
    st.session_state.valid[0] = validate_dropdown(st.session_state.type, [''])

    existingWarning = st.empty()

    if not st.session_state.valid[0] and st.session_state.clicks[0] > 0:
        with existingWarning.container():
            st.warning('Please select either new or existing client!')
    elif st.session_state.clicks[0] == 0:
        with existingWarning.container():
            st.markdown('<br style="margin:8px;">', unsafe_allow_html=True)
    else:
        existingWarning.empty()
        with existingWarning.container():
            st.markdown('')


    rightCol.selectbox('Client Office', [''] + [i for i in st.session_state.offices.OFFICENAME], key='office')
    st.session_state.valid[1] = validate_dropdown(st.session_state.office, [''])

    officeWarning = rightCol.empty()

    if not st.session_state.valid[1]:
        with officeWarning.container():
            st.warning('Please select an office for this client!')
    else:
        officeWarning.empty()

    leftCol.text_input('Client Name', 'Client Name', key='client')
    st.session_state.valid[2] = validate_string(st.session_state.client, ['Client Name'])

    nameWarning = leftCol.empty()

    if not st.session_state.valid[2]:
        with nameWarning.container():
            st.warning('Please enter a valid name for this client!')
    else:
        nameWarning.empty()

    if st.session_state.type == "New Client Relationship":
        rightCol.selectbox('Originator', [''] + [i for i in st.session_state.staff.EMPLOYEE], key='originator')
        st.session_state.valid[3] = validate_dropdown(st.session_state.originator, [''])

        originatorWarning = rightCol.empty()

        if not st.session_state.valid[3]:
            with originatorWarning.container():
                st.warning('Please select an originator for this client!')
        else:
            originatorWarning.empty()

    elif st.session_state.type == 'Subcode Needed for Existing Client':
        rightCol.selectbox('Client Relationship', [''] + [i for i in st.session_state.clients.CLIENTDISPLAY], key='relationship')
        st.session_state.valid[3] = validate_dropdown(st.session_state.relationship, [''])

        existingWarning = rightCol.empty()

        if not st.session_state.valid[3]:
            with existingWarning.container():
                st.warning('Please select a client relationship for this client!')
        else:
            existingWarning.empty()

    st.write(st.session_state.clicks)

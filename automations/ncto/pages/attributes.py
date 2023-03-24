from utilities.validators import validate_multi
# from utilities.click_handlers import inc_click - want to use to only render warnings after 

def screen(st):
    st.session_state.valid = [False]

    st.multiselect('Client Services', st.session_state.services.SERVTITLE, key='attributes_service')
    st.sessiion_state.valid[0] = validate_multi(st.session_state.attributes_service)

    warnings = st.expander('View warnings')

    if not st.session_state.valid[0]:
        with warnings:
            st.warning('Please select at least one service for this client!')
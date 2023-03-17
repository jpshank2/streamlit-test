def inc_click(st, position):
    st.session_state.clicks[position] = st.session_state.clicks[position] + 1

    st.write(st.session_state.clicks[position])
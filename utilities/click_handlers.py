def inc_click(st, position):
    updatedClicks = st.session_state.clicks
    updatedClicks[position] = updatedClicks[position] + 1

    st.session_state.clicks = updatedClicks
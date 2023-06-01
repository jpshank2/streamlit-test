from streamlit import session_state

def create_session(sessions):

    for session in sessions:
        if session[0] not in session_state:
            session_state[session[0]] = session[1]

    return True
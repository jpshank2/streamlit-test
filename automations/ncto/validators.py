def validate_dropdown(selection, notAllowed, valid):
    if selection == notAllowed:
        valid = False
    else:
        valid = True

    return valid
def validate_dropdown(selection, notAllowed, valid):
    if selection in notAllowed:
        valid = False
    else:
        valid = True

    return valid
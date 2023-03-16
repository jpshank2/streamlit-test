def validate_dropdown(selection, notAllowed):

    return False if selection in notAllowed else True

def validate_string(input, notAllowed):
    from re import search

    if search("\w", input) == None:
        return False
    else:
        return False if input in notAllowed else True

def validate_nums(input, minVal, maxVal):
    from re import search

    if search('\D', input) == None and len(input) >= minVal and len(input) <= maxVal:
        return True
    else:
        return True if len(input) >= minVal and len(input) <= maxVal else False
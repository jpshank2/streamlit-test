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

    if search('[^0-9]+', input) != None:
        return False
    elif search('\D', input) == None:
        if int(input) >= minVal and int(input) <= maxVal:
            return True
        else:
            return False
    else:
        return True if int(input) >= minVal and int(input) <= maxVal else False

def validate_email(input):
    from re import fullmatch

    if fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', input) == None:
        return False
    else:
        return True
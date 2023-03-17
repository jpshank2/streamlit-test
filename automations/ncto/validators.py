def validate_dropdown(selection, notAllowed):

    return False if selection in notAllowed else True

def validate_string(input, notAllowed):
    from re import search

    if search("\w", input) == None:
        return False
    else:
        return False if input in notAllowed else True

def validate_nums(minVal, maxVal, input=0):
    from re import search

    if search('\D', input) == None and int(input) >= minVal and int(input) <= maxVal:
        return True
    else:
        return True if int(input) >= minVal and int(input) <= maxVal else False
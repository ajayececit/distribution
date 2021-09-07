'''
Package where we can develop the common function which can be used for the
multiple modules.
'''

def check_and_convert_number(value, to_convert = False):
    try:
        value = int(value)
        if to_convert:
            return value
    except:
        return False
    return True

'''##################################################################################'''
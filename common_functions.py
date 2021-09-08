'''
Package where we can develop the common function which can be used for the
multiple modules.
'''
import os.path
from datetime import datetime

def check_and_convert_number(value, to_convert = False):
    try:
        value = float(value)
        if to_convert:
            return value
    except:
        return False
    return True

'''##################################################################################'''

def get_logger_file_name(file_path):
    if not file_path:
        return None
    try:
        homedir = os.path.expanduser("~")
        user_name = homedir.strip().split("\\")[-1]

        # calculate time and date for logger file
        time = datetime.now()
        from datetime import date
        today = date.today()
        current_time = time.strftime("%H_%M_%S")
        date = today.strftime("%d_%m_%Y")
        logger_run_time = date + "_" + current_time

        file_name = file_path.split("/")[-1]
        f_name, f_ext = os.path.splitext(file_name)
        logger_file_name = user_name + "_" + f_name +  "_" + \
                           "_logger_file_" + logger_run_time + ".log"
        return logger_file_name
    except:
        print(123)
        return None

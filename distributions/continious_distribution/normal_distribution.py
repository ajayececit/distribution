'''

Program to understand the topics and library usages of scipy and other ML libraries.
Problems i solved here are the problems given in the DS class on 5th-Sep-2021

using scipy.stats.norm to get the probability of X

'''

# importing library

from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import logging
import sys

import re

# Custom Functions
from common_functions import check_and_convert_number, get_logger_file_name

# Error Codes
mean_std_deviation_missing_error = "MEAN or STANDARD_DEVIATION is missing"
x_value_missing_error = "Didn't Provide Lower and Upper values of X"
input_error = "Not a Proper Input string to find the probability"
empty_probability_list_error = "Couldn't find Probablity List"
unknown_run_time_error = "Unknown Run Time Error"

# pattern used for regex
comparator_pattern= "\<\=|\>\=|\<|\>|="
greater_than_pattern = "\<\=X|\<X|X\>\=|X\>"

logger_file_name = get_logger_file_name(sys.argv[0])
if not logger_file_name:
    logger_file_name = "temp_file_logger.log"

logging.basicConfig(filename = logger_file_name,
                    format =' %(asctime)s %(message)s',
                    filemode = 'w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

'''##################################################################################'''

def validate_input(input_list):
    logger.info("*********************************************")
    logger.info(f"Running in validate_inputs and anaylising input {input_list}")
    logger.info("*********************************************")
    if not input_list:
        logger.error(empty_probability_list_error)
        return None, empty_probability_list_error

    # Main Condition

    if re.search('\<\=X|\<X|X\<\=|X\<', input_list[0]) and \
            re.search('\<\=X|\<X|X\<\=|X\<', input_list[-1]):
        logger.info("given input satisfied the condtion of a < X < b")
        return input_list, False

    # To handle the scenrio like
    # a > X < b
    # x < min(a, b)
    if re.search('\>\=X|\>X|X\<\=|X\<', input_list[0]) and \
            re.search('\>\=X|\>X|X\<\=|X\<', input_list[-1]):
        logger.info("given input are in the format of a > X < b \
                    so it will be fine if we can calculate the probablity \
                    for x < min(a, b)")
        pattern = '\>\=X|\>X|X\<\=|X\<'
        lower_x_pos = re.search(pattern, input_list[0])
        lower_x = input_list[0][:lower_x_pos.start()]
        upper_x_pos = re.search(pattern, input_list[-1])
        upper_x = input_list[-1][upper_x_pos.end():]

        if check_and_convert_number(lower_x, False) and \
                check_and_convert_number(upper_x, False):
            lower_x = check_and_convert_number(lower_x, True)
            upper_x = check_and_convert_number(upper_x, True)
            x_value = min(lower_x, upper_x)
            return ['X<' + str(x_value)], False

    # To handle the scenrio like
    # a < X > b
    # "30 < X > 35"
    # x < max(a, b)
    if re.search('\<\=X|\<X|X\>\=|X\>', input_list[0]) and \
            re.search('\<\=X|\<X|X\>\=|X\>', input_list[-1]):
        logger.info("given input are in the format of a < X > b \
                            so it will be fine if we can calculate the probablity \
                            for x < max(a, b)")
        pattern = '\<\=X|\<X|X\>\=|X\>'
        lower_x_pos = re.search(pattern, input_list[0])
        lower_x = input_list[0][:lower_x_pos.start()]
        upper_x_pos = re.search(pattern, input_list[-1])
        upper_x = input_list[-1][upper_x_pos.end():]

        if check_and_convert_number(lower_x, False) and \
                check_and_convert_number(upper_x, False):
            lower_x = check_and_convert_number(lower_x, True)
            upper_x = check_and_convert_number(upper_x, True)
            x_value = max(lower_x, upper_x)
            return ['X>' + str(x_value)], False

    # return the list with the probablity not happen as True
    # 30 > X > 35
    # have to subtract 1 from not final probablity
    logger.info("given input are in the format of a > X > b \
                                so we have to subtract 1 from the probablity, \
                                since it falls with the probablity not happen")
    return input_list, True


'''##################################################################################'''

def get_value_from_string(probability_string):
    try:
        probability_string = probability_string.upper()
        value = re.sub(comparator_pattern, "", probability_string.replace(" ", "").replace("X", ""))
        if check_and_convert_number(value, False):
            value = check_and_convert_number(value, True)
            return value
        else:
            return None
    except:
        return unknown_run_time_error

'''##################################################################################'''

def is_x_greater(x_string):
    try:
        if re.search(greater_than_pattern, x_string.replace(" ", "")):
            return True
        else:
            return False
    except:
        return unknown_run_time_error

'''##################################################################################'''

def probability_helper(mean, std_deviation, bound_list, prob_not_happen = False):

    '''

    :param mean: int
    :param std_deviation: int
    :param bound_list: the bound list of the probability (a < X < b, [a < X, X < b]
    :param prob_not_happen: in case if probability conds are a > X > b we have to
            subtract 1, because that can be do as 1 - P[a < X < b]
    :return: probability
    '''

    logger.info("*********************************************")
    logger.info(f"Running in probability_helper and processing for the z_value of the given /"
                f"probability conditions of  {bound_list}")
    logger.info("*********************************************")

    # using this pattern to find if X > a,
    # in such case we have to subrtact 1 from the final probability

    z_value_result = []
    for bound_value in bound_list:
        value = get_value_from_string(bound_value)

        if not value:
            logger.error(f"{input_error} in the function")
            return None, input_error
        # calculating the z_value by using the scipy function.
        z_value = norm(mean, std_deviation).cdf(value)

        # this logic is for, if the given inputs is X > a, we have to subtract 1
        if is_x_greater(bound_value) == unknown_run_time_error:
            return None, unknown_run_time_error
        if is_x_greater(bound_value) == True:
            if len(bound_list) == 1:
                z_value = 1 - z_value
        z_value_result.append(z_value)

    if len(z_value_result) == 2:
        if prob_not_happen: # return the prob with 1 - prob if it is probability of not happening
            return 1 - abs(z_value_result[-1] - z_value_result[0]), None
        return abs(z_value_result[-1] - z_value_result[0]), None # return difference of the probability
    return z_value_result[0], None # return the z_value which is stored in the list


'''##################################################################################'''

def split_probability_string(input_string):
    try:
        prob_to_find = []
        x_position = re.search('X|x', input_string)
        prob_to_find.append(input_string[:x_position.end()].replace(" ", "").strip())
        prob_to_find.append(input_string[x_position.start():].replace(" ", "").strip())
        return prob_to_find
    except:
        return None

'''##################################################################################'''

def probability_normal_distribution_string(mean, std_deviation, input_string):
    '''

    :param mean: int
    :param std_deviation: int
    :param input_string: string, probability condidion string, (a < X < b)
    :return: probability : int, final result which is the probability for the given condn
    '''

    logger.info("*********************************************")
    logger.info(f"Running in probability_normal_distribution_string"
                f" and processing to get the probablity of the given string /"
                f" {input_string}")
    logger.info("*********************************************")

    # Edge case/Corner Cases to validate the inputs
    if not input_string:
        logger.error(f"{input_error} in the function")
        return input_error

    if not mean or not std_deviation:
        logger.error(f"{mean_std_deviation_missing_error} in the function")
        return mean_std_deviation_missing_error

    if not re.search(comparator_pattern, input_string.replace(" ", "")):
        logger.error(f"{input_error} in the function")
        return input_error

    # get all the comparators are feed in the given input string.
    # if there are more than 2 comparators that are invalid and throwing an error
    comparator_lists = re.findall(comparator_pattern, input_string)

    if len(comparator_lists) > 2:
        logger.error(f"{input_error} in the function")
        return input_error
    prob_to_find = []

    if len(comparator_lists) == 2:
        prob_to_find = split_probability_string(input_string)
        if not prob_to_find:
            logger.error("getting error !! ")
            logger.error(f"{unknown_run_time_error} in the function")
            return unknown_run_time_error
        prob_to_find, prob_not_happen = validate_input(prob_to_find)

        if not prob_to_find:
            logger.error("getting error !! ")
            logger.error(f"{prob_not_happen} in the function")
            return prob_not_happen

        if prob_to_find:
            probablity, err = probability_helper(mean, std_deviation, prob_to_find, prob_not_happen)
            if err:
                logger.error("getting error !! ")
                logger.error(f"{err} in the function")
                return err

        logger.info("---------------------------------------------")
        logger.info(f"Probability for the condition {input_string}, with the mean "
                    f"{mean} and std_deviation as {std_deviation} is : {round(probablity, 5)} ")
        logger.info("---------------------------------------------")
        return round(probablity, 5)

    if len(comparator_lists) == 1:
        prob_to_find.append(input_string.replace(" ", "").strip())
        probablity, err = probability_helper(mean, std_deviation, prob_to_find, False)
        if err:
            logger.error("getting error !! ")
            logger.error(f"{err} in the function")
            return err
        logger.info("---------------------------------------------")
        logger.info(f"Probability for the condition {input_string}, with the mean "
                    f"{mean} and std_deviation as {std_deviation} is : {round(probablity, 5)} ")
        logger.info("---------------------------------------------")
        return round(probablity, 5)


'''##################################################################################'''

def probability_normal_distribution(mean, std_deviation, lower_x = None, upper_x = None):

    '''
    :param mean: int
    :param std_deviation: int
    :param lower_x: int
    :param upper_x: int
    :return: normal_distribution of the given X, Mean and Std Deviation
    '''

    if not mean or not std_deviation:
        logger.error(f"{mean_std_deviation_missing_error} in the function")
        return mean_std_deviation_missing_error

    if lower_x is None and upper_x is None:
        logger.error(f"{x_value_missing_error} in the function")
        return x_value_missing_error

    if upper_x is None:
        upper_x = lower_x
        lower_x = None

    if upper_x and lower_x:
        lower_z_score = norm(mean, std_deviation).cdf(lower_x)  # Cumulative Distributed Function/Z Value
        upper_z_score = norm(mean, std_deviation).cdf(upper_x)  # Cumulative Distributed Function/Z Value
        return abs(upper_z_score - lower_z_score)

    if lower_x is None:
        z_value = norm(mean, std_deviation).cdf(upper_x)     # Cumulative Distributed Function/Z Value
        return z_value

'''##################################################################################'''

def generate_standard_score(mean, std_deviation, value):
    logger.info("*********************************************")
    logger.info(f"Running in generate_standard_score"
                f" to find the standard_score or z-score of/"
                f" {value}")
    logger.info("*********************************************")

    if not value:
        return None

    if not input_string:
        logger.error(f"{input_error} in the function")
        return None, input_error

    if not mean or not std_deviation:
        logger.error(f"{mean_std_deviation_missing_error} in the function")
        return None, mean_std_deviation_missing_error

    if not re.search(comparator_pattern, input_string.replace(" ", "")):
        logger.error(f"{input_error} in the function")
        return None, input_error

    try:
        z_score = (value - mean)/std_deviation
        return z_score, None
    except:
        return None, unknown_run_time_error

'''##################################################################################'''

def plot_distribution_graph_helper(mean, std_deviation, input_string, comparator_lists):

    try:
        prob_to_find = []

        if len(comparator_lists) == 2:
            prob_to_find = split_probability_string(input_string)
            if not prob_to_find:
                logger.error("getting error !! ")
                logger.error(f"{unknown_run_time_error} in the function")
                return unknown_run_time_error
            prob_to_find, prob_not_happen = validate_input(prob_to_find)

            if not prob_to_find:
                logger.error("getting error !! ")
                logger.error(f"{prob_not_happen} in the function")
                return prob_not_happen

        if len(comparator_lists) == 1:
            prob_to_find.append(input_string.replace(" ", "").strip())
            if is_x_greater(input_string) == unknown_run_time_error:
                return None, unknown_run_time_error
            if is_x_greater(input_string) == True:
                prob_not_happen = True
            else:
                prob_not_happen = False


        value_list = []
        standard_score_list = []
        if prob_to_find:
            for prob in prob_to_find:
                value = get_value_from_string(prob)
                if not value:
                    logger.error(f"{input_error} in the function")
                    return None, input_error
                if value == unknown_run_time_error:
                    return unknown_run_time_error

                value_list.append(value)
                standard_score, err = generate_standard_score(mean, std_deviation, value)
                if err:
                    return err

                if is_x_greater(prob) == unknown_run_time_error:
                    return None, unknown_run_time_error
                if is_x_greater(prob) == True:
                    standard_score_list.append((standard_score, True, prob_not_happen))
                else:
                    standard_score_list.append((standard_score, False, prob_not_happen))

        if len(standard_score_list) == 1:
            standard_score_list.append((None, False, False))

        return standard_score_list
    except:
        return unknown_run_time_error

'''##################################################################################'''
def plot_distribution_graph(mean, std_deviation, input_string):
    '''

        :param mean:
        :param std_deviation:
        :param input_string:
        :return:
        '''

    logger.info("*********************************************")
    logger.info(f"Running in plot_distribution_graph"
                f"to plot the distribution graph /"
                f" {input_string}")
    logger.info("*********************************************")

    # Edge case/Corner Cases to validate the inputs
    if not input_string:
        logger.error(f"{input_error} in the function")
        return input_error

    if not mean or not std_deviation:
        logger.error(f"{mean_std_deviation_missing_error} in the function")
        return mean_std_deviation_missing_error

    if not re.search(comparator_pattern, input_string.replace(" ", "")):
        logger.error(f"{input_error} in the function")
        return input_error

    # get all the comparators are feed in the given input string.
    # if there are more than 2 comparators that are invalid and throwing an error
    comparator_lists = re.findall(comparator_pattern, input_string)

    if len(comparator_lists) > 2:
        logger.error(f"{input_error} in the function")
        return input_error

    standard_score_list = plot_distribution_graph_helper(mean, std_deviation, input_string, comparator_lists)

    if standard_score_list == unknown_run_time_error:
        return unknown_run_time_error

    probability = probability_normal_distribution_string(mean, std_deviation, input_string)
    prob_x_start_range = standard_score_list[0][0]
    prob_x_end_range = standard_score_list[1][0]

    second_fill_flag = False
    if standard_score_list[0][2] == True and \
            standard_score_list[1][2] == True:
        second_fill_flag = True

        if standard_score_list[0][1] == False:
            prob_x_start_range = -4
            prob_x_end_range = standard_score_list[0][0]
        else:
            prob_x_start_range = standard_score_list[0][0]
            prob_x_end_range = 4

        if standard_score_list[1][1] == False:
            prob_x1_start_range = -4
            prob_x1_end_range = standard_score_list[1][0]
        else:
            prob_x1_start_range = standard_score_list[1][0]
            prob_x1_end_range = 4

    if prob_x_end_range == None:
        prob_not_happen = standard_score_list[0][2]
        if not prob_not_happen:
            prob_x_end_range = prob_x_start_range
            prob_x_start_range = -4
        else:
            prob_x_end_range = 4

    probability_x_axis = np.arange(prob_x_start_range, prob_x_end_range, 0.001)
    probability_y_axis = norm.pdf(probability_x_axis, 0, 1)

    if second_fill_flag:
        probability_x1_axis = np.arange(prob_x1_start_range, prob_x1_end_range, 0.001)
        probability_y1_axis = norm.pdf(probability_x1_axis, 0, 1)

    whole_x_axis = np.arange(-10, 10, 0.001)
    whole_y_axis = norm.pdf(whole_x_axis, 0, 1)

    fig, ax = plt.subplots(figsize=(9, 6))
    plt.style.use('fivethirtyeight')
    ax.plot(whole_x_axis, whole_y_axis)

    ax.fill_between(probability_x_axis, probability_y_axis, 0, alpha=0.3, color='red')
    ax.fill_between(whole_x_axis, whole_y_axis, 0, alpha=0.1, color="w")

    if second_fill_flag:
        ax.fill_between(probability_x1_axis, probability_y1_axis, 0, alpha=0.3, color='red')
        second_fill_flag = False

    ax.set_xlim([-4, 4])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    ax.set_title('Normal Gaussian Curve')

    # plt.savefig('normal_curve.png', dpi=72, bbox_inches='tight')
    plt.text(-3, 0.3, "Probability: \n" + str(probability), fontsize=22)

    plt.show()
    return


'''##################################################################################'''
if __name__ == '__main__':
    mean = 50000
    std_deviation = 20000
    lower_x = None
    upper_x = None
    input_string = "X > 70000"
    test = probability_normal_distribution_string(mean, std_deviation, input_string)
    print(test)
    # result = probability_normal_distribution(mean, std_deviation, lower_x, upper_x)
    # print(result)
    print(test)
    plot_distribution_graph(mean, std_deviation, input_string)
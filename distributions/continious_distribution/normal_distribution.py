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
from datetime import datetime, date
import re

# Custom Functions
from common_functions import check_and_convert_number

# Error Codes
mean_std_deviation_missing_error = "MEAN or STANDARD_DEVIATION is missing"
x_value_missing_error = "Didn't Provide Lower and Upper values of X"
input_error = "Not a Proper Input string to find the probability"
comparator_pattern= "\<\=|\>\=|\<|\>|="

# calculate time and date for logger file
time = datetime.now()
date = date.today()
current_time = time.strftime("%H_%M_%S")
date = date.strftime("%d_%m_%Y")
logger_run_time = date + "_" + current_time
logger_file_name = "logger_file_" + logger_run_time + ".log"

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
        logger.error("Couldn't find Probablity List")
        return

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


def test_func(mean, std_deviation, bound_list, prob_not_happen = False):

    '''

    :param mean: int
    :param std_deviation: int
    :param bound_list: the bound list of the probability (a < X < b, [a < X, X < b]
    :param prob_not_happen: in case if probability conds are a > X > b we have to
            subtract 1, because that can be do as 1 - P[a < X < b]
    :return: probability
    '''

    logger.info("*********************************************")
    logger.info(f"Running in test_func and processing for the z_value of the given /"
                f"probability conditions of  {bound_list}")
    logger.info("*********************************************")

    # using this pattern to find if X > a,
    # in such case we have to subrtact 1 from the final probability
    greater_than_pattern = "\<\=X|\<X|X\>\=|X\>"
    z_value_result = []

    for bound_value in bound_list:
        value = re.sub(comparator_pattern, "", bound_value.replace(" ", "").replace("X", ""))
        if check_and_convert_number(value, False):
            value = check_and_convert_number(value, True)
        else:
            logger.error(f"{input_error} with the given input : {value}")
            return input_error

        # calculating the z_value by using the scipy function.
        z_value = norm(mean, std_deviation).cdf(value)

        # this logic is for, if the given inputs is X > a, we have to subtract 1
        if re.search(greater_than_pattern, bound_value.replace(" ", "")):
            z_value = 1 - z_value
        z_value_result.append(z_value)

    if len(z_value_result) == 2:
        if prob_not_happen: # return the prob with 1 - prob if it is probability of not happening
            return 1 - abs(z_value_result[-1] - z_value_result[0])
        return abs(z_value_result[-1] - z_value_result[0]) # return difference of the probability
    return z_value_result[0] # return the z_value which is stored in the list


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
        x_position = re.search('X|x', input_string)
        prob_to_find.append(input_string[:x_position.end()].replace(" ", "").strip())
        prob_to_find.append(input_string[x_position.start():].replace(" ", "").strip())
        prob_to_find, prob_not_happen = validate_input(prob_to_find)

        if prob_to_find:
            probablity = test_func(mean, std_deviation, prob_to_find, prob_not_happen)
        logger.info("---------------------------------------------")
        logger.info(f"Probability for the condition {input_string}, with the mean "
                    f"{mean} and std_deviation as {std_deviation} is : {probablity} ")
        logger.info("---------------------------------------------")
        return probablity

    if len(comparator_lists) == 1:
        prob_to_find.append(input_string.replace(" ", "").strip())
        probablity = test_func(mean, std_deviation, prob_to_find, False)
        logger.info("---------------------------------------------")
        logger.info(f"Probability for the condition {input_string}, with the mean "
                    f"{mean} and std_deviation as {std_deviation} is : {probablity} ")
        logger.info("---------------------------------------------")
        return probablity


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

def plot_std_normal_distribution():
    mean = 0
    std_deviation = 1
    x = np.linspace(mean - 3 * std_deviation, mean + 3 * std_deviation, 100)
    plt.plot(x, norm.pdf(x, mean, std_deviation), color='black')
    # plt.fill_between([1], [1])
    plt.show()

'''##################################################################################'''

if __name__ == '__main__':
    mean = 30
    std_deviation = 4
    lower_x = 30
    upper_x = 35
    input_string = "30 < X < 35"
    test = probability_normal_distribution_string(mean, std_deviation, input_string)
    print(test)
    result = probability_normal_distribution(mean, std_deviation, lower_x, upper_x)
    print(result)
    # print(norm(mean, std_deviation).sf(0.394350226))
    # plot_std_normal_distribution()v
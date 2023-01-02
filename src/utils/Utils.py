import logging
import os
import sys
import pandas as pd
from fake_useragent import UserAgent
import random


def get_logger():
    return logging.getLogger()


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def convert_input_into_list(*params):
    converted_params = list()
    for param in params:

        if param is not None:
            if not isinstance(param, list):
                if isinstance(param, dict):
                    param = list(param.keys())
                elif isinstance(param, str) or isinstance(param, int):
                    param = [param]
                else:
                    try:
                        param = list(param)
                    except Exception as err:
                        print(f"CAUTION! Some items could not converted into 'list' type: {param}")
                        print(err)
                        param = list()
        converted_params.append(param)

    return tuple(converted_params)


def convert_input_into_int_list(*params_list):
    converted_params_lists = list()
    for param in params_list:
        if param is not None:
            if isinstance(param, list):
                temp_params_list = list()
                for item in param:
                    try:
                        item = int(item)
                    except Exception as err:
                        print(f"CAUTION! Some items could not converted into 'int' type: {item}")
                        print(err)
                    temp_params_list.append(item)
            else:
                temp_params_list = param
            converted_params_lists.append(temp_params_list)
        else:
            converted_params_lists.append(None)
    return tuple(converted_params_lists)


def convert_input_into_str_list(*params, remove_char=""):
    converted_params = list()
    for param in params:
        temp_param = None
        if param is not None:
            if hasattr(param, "__getitem__"):
                temp_param = list()
                for item in param:
                    try:
                        temp_param.append(str(item).replace(remove_char, ""))
                    except Exception as err:
                        print(f"CAUTION! Some items could not converted into str type: {item}")
                        print(err)
                        temp_param.append(item)
        converted_params.append(temp_param)
    return tuple(converted_params)


def loading_bar(norm, current_index, print_result=False, percentage=100, percentage_notation="%"):
    loading_string = "Loading: "
    result = None
    if isinstance(percentage_notation, str):
        loading_string += str(percentage_notation) + "{}"
    else:
        loading_string += "{}"

    if norm != 0 and current_index >= 0:
        result = int(float(1/norm) * int(current_index) * percentage)

    if print_result:
        print(loading_string.format(str(result)))
    return result


def path_append_up_to_src_file(child_directory=str()):
    norm = len(os.getcwd().split("\\"))
    temp_path = os.getcwd()
    for i in range(norm):
        temp_path = os.path.split(temp_path)
        if temp_path[1] == "src":
            parent_path = os.path.abspath(temp_path[0])
            sys.path.append(parent_path)
            result = parent_path + child_directory
            return result

        temp_path = os.path.abspath(temp_path[0])


def concat_data_frames(data_frame_list, fill_nan_values=None, drop_non_values=True, reset_df_index=None):
    if not isinstance(data_frame_list, list):
        data_frame_list = [data_frame_list]

    concated_data_frame = pd.concat(data_frame_list)

    if concated_data_frame.isna().sum().sum() > 0:
        if fill_nan_values:
            concated_data_frame.fillna(value=fill_nan_values, inplace=True)
            print("There were nan values in the data frame and they have been replaced with, " + fill_nan_values)
        elif drop_non_values:
            concated_data_frame.dropna(inplace=True)
            print("There were nan values in the data frame and they have been dropped.")
        else:
            print("CAUTION: There are nan values in the merged data frame.")

    if reset_df_index:
        mapper = {"index": "player"}
        if "mapper" in reset_df_index:
            if reset_df_index["mapper"]:
                mapper = reset_df_index["mapper"]
        concated_data_frame.reset_index(inplace=True)
        concated_data_frame.rename(mapper=mapper, axis=1, inplace=True)

    return concated_data_frame


def merge_data_frames_by_assigning_ones_and_zeros(data_frame_list_for_assigning_ones,
                                                  data_frame_list_for_assigning_zeros,
                                                  ones_zeros_column_name="One or Zero"):
    if not isinstance(data_frame_list_for_assigning_ones, list):
        data_frame_list_for_assigning_ones = [data_frame_list_for_assigning_ones]

    if not isinstance(data_frame_list_for_assigning_zeros, list):
        data_frame_list_for_assigning_zeros = [data_frame_list_for_assigning_zeros]

    all_frames = list()

    for data_frame in data_frame_list_for_assigning_ones:
        data_frame[ones_zeros_column_name] = 1
        all_frames.append(data_frame)

    for data_frame in data_frame_list_for_assigning_zeros:
        data_frame[ones_zeros_column_name] = 0
        all_frames.append(data_frame)

    return pd.concat(all_frames)


def get_optimal_user_agent(browser_name=None, max_count=10, test_url='https://www.google.com/'):
    count = 0
    user_agent = None

    def _choose_fake_user_agent(candidate_browser_name):
        candidate_user_agent = UserAgent()
        if isinstance(candidate_browser_name, str):
            candidate_browser_name = candidate_browser_name.strip()
        elif hasattr(candidate_browser_name, "__getitem__"):
            candidate_browser_name = random.choice(candidate_browser_name)
        else:
            return candidate_user_agent.random
        return candidate_user_agent[candidate_browser_name]

    while user_agent is None and count <= max_count:
        temp_user_agent = _choose_fake_user_agent(candidate_browser_name=browser_name)
        temp_status_code = requests.get(test_url, headers={"User-Agent": temp_user_agent}).status_code
        if temp_status_code == 200:
            user_agent = temp_user_agent
            print(f"Fake user agent has been created at the attempt {count}, named as {user_agent}")
        else:
            count += 1

    if user_agent is None:
        print("The user agent could not be chosen, please check the test_url or try to specify name of the browser.")

    return user_agent


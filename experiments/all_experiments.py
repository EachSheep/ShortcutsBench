"""
1. Test Experiment 1: Evaluate the ability to select the correct API, without assessing parameters.
2. Test Experiment 2: Assess the correct population of primitive data types/enumerations.
3. Test Experiment 3: Evaluate the correctness of system or user inputs.
"""

import json
import os
import random
import time
import re
import openai
import copy
from collections import defaultdict
import logging
import tiktoken
import dashscope
import argparse
import google.generativeai as genai

from generate_shortcut_desc import APIsClass, WFActionsClass, get_identifier2return_value, get_all_shortcuts_paras_that_is_necessary_in_query
from cal_shortcut_len import cal_WFWorkflowActions_len, label_each_WFWorkflowAction_pos_inplace
from all_experiments_prompt import SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA")

# MODEL_NAME = 'gemini-1.5-pro' # $3.5 / 1M, $10.5 / 1M
# MODEL_NAME = 'qwen2-72b-instruct' # 5 / 1M, 10 / 1M => exchange_rate : 7.1151 => 0.70 / 1M, 1.40 / 1M 
# MODEL_NAME = 'deepseek-chat'  # $0.14 / 1M, $0.28 / 1M
# MODEL_NAME = 'deepseek-coder' # $0.14 / 1M, $0.28 / 1M
# MODEL_NAME = 'meta-llama/Llama-3-70b-chat-hf' # $1.17 / 1M, $1.17 / 1M
# MODEL_NAME = 'gemini-1.5-flash' # $0.35 / 1M, $1.05 / 1M
# MODEL_NAME = 'qwen2-57b-a14b-instruct' # 3.5 / 1M, 7 / 1M  => exchange_rate : 7.1151 => 0.49 / 1M, 0.98 / 1M 
# MODEL_NAME = "gpt-3.5-turbo" # $0.50 / 1M, $1.50 / 1M
# MODEL_NAME = 'GLM-4-Air' # 1 / 1M, 1 / 1M => exchange_rate : 7.1151 => 0.14 / 1M, 0.14 / 1M 
# https://aimlapi.com/comparisons/llama-3-vs-chatgpt-3-5-comparison

ignore_in_judge_WFWorkflowActionIdentifier_list = [  # Actions not included in the evaluation results
    "is.workflow.actions.conditional",
    "is.workflow.actions.choosefrommenu",
    "is.workflow.actions.repeat.each",
    "is.workflow.actions.repeat.count",
    "is.workflow.actions.getvariable",
    "is.workflow.actions.setvariable",
    "is.workflow.actions.appendvariable",
    "is.workflow.actions.runworkflow",
    "is.workflow.actions.gettext",
    "is.workflow.actions.ask"
]
filter_WFWorkflowActionIdentifier_list = [  # Directly excluded: not included in the evaluation results and not used as input for the agent (the agent does not see this comment).
    "is.workflow.actions.comment",
    "is.workflow.actions.alert"
]

branch_num_2_nlp_desc = {  # Map the parameters of `is.workflow.actions.conditional` for model interpretation.
    "0": '"less/earlier than"',
    "1": '"less than or equal"',
    "2": '"greater/later than"',
    "3": '"greater than or equal"',
    "4": '"is"',
    "5": '"is not"',
    "8": '"begin with"',
    "9": '"end with"',
    "99": '"contain"',
    "100": '"have value"',
    "101": '"do not have any value"',
    "999": '"do not contain"',
    "1000": '"is after"',
    "1001": '"is the most recent"',
    "1002": '"is today"',
    "1003": '"is between"',
    "Contains": '"contains"',
    "Equals": '"equals"',
    "Is Less Than": '"is less than"',
    "Is Greater Than": '"is greater than"'
}

def extract_json(text):
    # Match the outermost curly braces and their contents.
    pattern = r"\{.*\}"
    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        try:
            # Attempt to parse the matched string as a JSON object.
            json_object = json.loads(match.group())
            return json.dumps(json_object, indent=2)  # Format the output.
        except json.JSONDecodeError:
            continue

    return None


def match_brackets(text):
    # Match the outermost curly braces and their contents.
    pattern = r"\{.*\}"
    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        try:
            # Try to parse the matched string as a JSON object.
            json_object = json.loads(match.group())
            return json.dumps(json_object, indent=2)  # Format the output.
        except json.JSONDecodeError:
            continue

    return text

class APIBasedAgent:

    def __init__(self, all_api_descs_dict):

        # Each element is a dictionary: `{'APIName': api_name, 'Description': api_description}`.
        self.all_api_descs_dict = all_api_descs_dict
        self.all_api_descs_list = [f"{i + 1}. {api_name}. {api_description}" for i,
                                   (api_name, api_description) in enumerate(self.all_api_descs_dict.items())]
        self.all_api_descs = "\n".join(self.all_api_descs_list)
        self.all_api_names = list(self.all_api_descs_dict.keys())

        self.history_actions = []

    def set_history_actions(self, history_actions):
        self.history_actions = history_actions
        self.history_actions = traverse_and_truncate(self.history_actions)

    def append_history_actions(self, history_action):
        history_action = traverse_and_truncate(self.history_actions)
        self.history_actions.append(history_action)

    def get_history_action_str(self):
        return json.dumps(self.history_actions, indent=2)


def truncate_string(value, max_length=300):
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length] + '...'
    return value


def traverse_and_truncate(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = traverse_and_truncate(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = traverse_and_truncate(data[i])
    else:
        data = truncate_string(data)
    return data


def get_all_api_info():
    """Retrieve information for all APIs, i.e., a mapping from API names to API descriptions.
    """

    # Load all API information from `WFActions.json`.
    WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions",
                                  "WorkflowKit.framework/Versions/A/Resources/WFActions.json")
    wf_actions_instance = WFActionsClass(WFActions_path)
    my_WFActions_path = os.path.join(
        SHORTCUT_DATA, "is.workflow.actions", "my_WFActions.json")
    wf_actions_instance.WFActions_dicts.update(
        json.load(open(my_WFActions_path, "r")))
    all_api2info_WF, all_api2paraname2paratype_WF, all_api2parasummary_WF = wf_actions_instance.all_api2desc(
        need_api2paraname2paratype=True, need_api2parasummary=True)
    # Load all API information from the app.
    # succ_api_json_path = os.path.join(
    #     SHORTCUT_DATA, "4_success_api_json_filter.json")
    # fail_api_json_path = os.path.join(
    #     SHORTCUT_DATA, "4_fail_api_json_filter.json")
    # API_instance = APIsClass(
    #     succ_api_json_path, fail_api_json_path)
    api_json_path = os.path.join(
        SHORTCUT_DATA, "4_api_json_filter.json")
    API_instance = APIsClass(api_json_path)
    all_api2info_from_app, all_api2paraname2paratype_from_app, _ = API_instance.all_api2desc(
        need_api2paraname2paratype=True, need_api2parasummary=True)
    """Mapping of all APIs to their information."""
    all_api2info = all_api2info_WF.copy()
    all_api2info.update(all_api2info_from_app)

    """Mapping of all APIs to parameter names to parameter types (including default values)."""
    all_api2paraname2paratype = all_api2paraname2paratype_WF.copy()
    all_api2paraname2paratype.update(all_api2paraname2paratype_from_app)

    return all_api2info, all_api2paraname2paratype


def sample_more_APIs(all_api2info, number, exclude_APIs=[]):
    """Randomly select `number` APIs from all available APIs.
    """
    if number <= 0:
        return []

    all_APIs = list(all_api2info.keys())
    # Compute the difference set.
    all_APIs = list(set(all_APIs) - set(exclude_APIs))
    sampled_APIs = random.sample(all_APIs, number)
    return sampled_APIs


def remove_wf_serialization_types(data):
    if isinstance(data, dict):
        remove_keys = []
        for key, value in data.items():
            if key == "WFSerializationType":
                remove_keys.append(key)
            else:
                remove_wf_serialization_types(value)
        for key in remove_keys:
            del data[key]
    elif isinstance(data, list):
        for item in data:
            remove_wf_serialization_types(item)


def count_and_clean_aggrandizements(data, type_counts=None):
    """Count the distinct values for the key `"Type"` in all dictionaries and the frequency of each value. 
    After counting, delete dictionaries with keys `WFCoercionVariableAggrandizement`, `WFDateFormatVariableAggrandizement`, 
    and `WFUnitVariableAggrandizement`. If `Aggrandizements` is empty after these deletions, also remove `Aggrandizements`.
    """

    if type_counts is None:
        type_counts = defaultdict(int)

    if isinstance(data, dict):
        keys_to_remove = []
        for key, value in data.items():
            if key == "Aggrandizements" and isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict) and "Type" in item:
                        type_counts[item["Type"]] += 1
                        if item["Type"] not in ["WFCoercionVariableAggrandizement", "WFDateFormatVariableAggrandizement", "WFUnitVariableAggrandizement"]:
                            new_list.append(item)
                    else:
                        new_list.append(item)
                data[key] = new_list
                if not data[key]:
                    keys_to_remove.append(key)
            else:
                count_and_clean_aggrandizements(value, type_counts)

        for key in keys_to_remove:
            del data[key]

    elif isinstance(data, list):
        for item in data:
            count_and_clean_aggrandizements(item, type_counts)

    return type_counts


def replace_and_sort_attachments(data):
    """Find all dictionaries where the values include both the keys `string` and `attachmentsByRange`. 
    Replace all instances of `￼` in `string` with `${ValueXX}`, 
    where XX is a sequential number starting from 1. 
    Then, replace all `attachmentsByRange` keys with `ValueXX`. 
    Note that you first need to sort `attachmentsByRange` keys numerically based on the number XX1 in keys like `{XX1,XX2}`.
    """

    def process_internal(data):
        if "string" in data and "attachmentsByRange" in data:
            # Replace ￼ with ${ValueXX} in "string"
            value_index = 1
            data["string"] = re.sub(
                r"￼", lambda _: f"${{Value{value_index}}}", data["string"])
            value_index += 1

            # Sort attachmentsByRange by the first number in the key
            sorted_attachments = sorted(data["attachmentsByRange"].items(
            ), key=lambda item: int(re.search(r'\{(\d+),', item[0]).group(1)))

            # Create a new dictionary for sorted attachments with new keys
            new_attachments = {}
            for idx, (key, value) in enumerate(sorted_attachments):
                new_key = f"Value{idx + 1}"
                new_attachments[new_key] = value

            data["attachmentsByRange"] = new_attachments

        for key, value in data.items():
            if isinstance(value, (dict, list)):
                replace_and_sort_attachments(value)

    if isinstance(data, dict):
        process_internal(data)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                replace_and_sort_attachments(item)

    return data

categorie2num_dict = {
    "Productivity & Utilities": 0,
    "Health & Fitness": 1,
    "Entertainment & Media": 2,
    "Lifestyle & Social": 3,
    "Education & Reference": 4,
    "Business & Finance": 5,
    "Development & API": 6,
    "Home & Smart Devices": 7
}

def evaluate_experiment1(shortcuts_list, print_or_not = True):
    """Evaluation of Question 1 focuses solely on whether the correct API was selected, without considering the parameters.

    Each element is a dictionary：{
        "URL": URL,
        "query": log_query,
        "api_names": log_api_names,
        "api_descs": log_api_descs,
        "aseqs": aseqs,
        "bseqs": bseqs,
        "cur_input_token_count": cur_input_token_count,
        "cur_output_token_count": cur_output_token_count,
        "cur_input_cost": cur_input_cost,
        "cur_output_cost": cur_output_cost,
        "cur_total_cost": cur_total_cost
    }
    """
    if print_or_not:
        print("Begin evaluating Experiment 1: focus only on whether the correct API was selected, ignoring the parameters.")

    with open(os.path.join(SHORTCUT_DATA, f"generated_success_categories.json"), "r") as f:
        generated_success_categories = json.load(f)

    aseq_res_list = []
    bseq_res_list = []

    """
    1. <=1
    2. (1, 5]
    3. (5, 15]
    4. (15, 30]
    """

    for cur_shortcut_dict in shortcuts_list:
        URL = cur_shortcut_dict["URL"]
        aseqs = cur_shortcut_dict["aseqs"]  # Actual actions
        aseq_len = cal_WFWorkflowActions_len(aseqs, URL)
        bseqs = cur_shortcut_dict["bseqs"]  # Generated actions, corresponding one-to-one with `aseqs`.
        all_api_names = cur_shortcut_dict["api_names"] # All APIs available to the agent
        true_api_names = []
        for aseq in aseqs:
            true_api_names.append(aseq["WFWorkflowActionIdentifier"])

        label_each_WFWorkflowAction_pos_inplace(aseqs, URL)

        for aseq, bseq in zip(aseqs, bseqs):
            WFWorkflowActionIdentifier = aseq["WFWorkflowActionIdentifier"]
            if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                continue
            if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                continue

            aseq_res_list.append(
                {"URL": URL, "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier, "len_aseq": aseq_len})
            if "pos" in aseq:
                aseq_res_list[-1]["pos"] = aseq["pos"] # `pos` refers to the position of the current action within the current shortcut.
            aseq_res_list[-1]["all_api_names"] = all_api_names
            aseq_res_list[-1]["true_api_names"] = true_api_names

            if bseq["state"] == "json_error" or bseq["state"] == "generated_by_agent" and "WFWorkflowActionIdentifier" not in bseq["aseq"]:
                bseq_res_list.append(
                    {"URL": URL, "WFWorkflowActionIdentifier": None, "len_aseq": aseq_len})
                continue

            WFWorkflowActionIdentifier_pred = bseq["aseq"]["WFWorkflowActionIdentifier"]
            bseq_res_list.append(
                {"URL": URL, "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier_pred, "len_aseq": aseq_len})

    # Calculate the overall accuracy of `aseq_res_list` and `bseq_res_list`, as well as the accuracy within each of the four interval ranges.
    correct_num, all_num = 0, 0
    correct_num_list = [0, 0, 0, 0]
    all_num_list = [0, 0, 0, 0]
    categories_correct_num = [0] * len(categorie2num_dict) 
    categories_all_num = [0] * len(categorie2num_dict)
    # The x-axis represents the action's position in the shortcut, while the y-axis represents accuracy. Each model is represented by a separate line.
    correct_num_every_len_level2, all_num_every_len_level2 = {}, {}
    correct_num_every_len_level3, all_num_every_len_level3 = {}, {}
    correct_num_every_len_level4, all_num_every_len_level4 = {}, {}
    # The x-axis represents different models, and the y-axis represents accuracy. 
    # The bar chart displays five intervals for each bar: (0,5], (5,10], (10,15], (15,20], and (20,+), 
    # indicating the number of APIs available to the agent.
    correct_num_api_nums = [0] * 5
    all_num_api_nums = [0] * 5
    hall_numerator = [0] * 5 # The API selected by the model is not among the APIs available to the agent.
    percentage_numerator = [0] * 5 # The location of the APIs favored by the model.
    percentage_denominator = [0] * 5 # The positions of APIs preferred by the model.

    for aseq_dict, bseq_dict in zip(aseq_res_list, bseq_res_list):
        URL = aseq_dict["URL"]
        if aseq_dict["WFWorkflowActionIdentifier"] == bseq_dict["WFWorkflowActionIdentifier"]:
            correct_num += 1
            if aseq_dict["len_aseq"] <= 1:
                correct_num_list[0] += 1
            elif 1 < aseq_dict["len_aseq"] <= 5:
                correct_num_list[1] += 1
                if 'pos' in aseq_dict:
                    correct_num_every_len_level2[aseq_dict["pos"]] = correct_num_every_len_level2.get(aseq_dict["pos"], 0) + 1
            elif 5 < aseq_dict["len_aseq"] <= 15:
                correct_num_list[2] += 1
                if 'pos' in aseq_dict:
                    correct_num_every_len_level3[aseq_dict["pos"]] = correct_num_every_len_level3.get(aseq_dict["pos"], 0) + 1
            elif 15 < aseq_dict["len_aseq"] <= 30:
                correct_num_list[3] += 1
                if 'pos' in aseq_dict:
                    correct_num_every_len_level4[aseq_dict["pos"]] = correct_num_every_len_level4.get(aseq_dict["pos"], 0) + 1
            
            if len(aseq_dict["all_api_names"]) <= 5:
                correct_num_api_nums[0] += 1
            elif 5 < len(aseq_dict["all_api_names"]) <= 10:
                correct_num_api_nums[1] += 1
            elif 10 < len(aseq_dict["all_api_names"]) <= 15:
                correct_num_api_nums[2] += 1
            elif 15 < len(aseq_dict["all_api_names"]) <= 20:
                correct_num_api_nums[3] += 1
            else:
                correct_num_api_nums[4] += 1

            if URL in generated_success_categories:
                category = generated_success_categories[URL]['category']
                if category in categorie2num_dict:
                    categories_correct_num[categorie2num_dict[category]] += 1
        else:
            if len(aseq_dict["all_api_names"]) <= 5:
                if bseq_dict["WFWorkflowActionIdentifier"] not in aseq_dict["all_api_names"]:
                    hall_numerator[0] += 1
                else:
                    chose_pos = aseq_dict["all_api_names"].index(bseq_dict["WFWorkflowActionIdentifier"])
                    percentage_numerator[0] += chose_pos / len(aseq_dict["all_api_names"])
                percentage_denominator[0] += 1
            elif 5 < len(aseq_dict["all_api_names"]) <= 10:
                if bseq_dict["WFWorkflowActionIdentifier"] not in aseq_dict["all_api_names"]:
                    hall_numerator[1] += 1
                else:
                    chose_pos = aseq_dict["all_api_names"].index(bseq_dict["WFWorkflowActionIdentifier"])
                    percentage_numerator[1] += chose_pos / len(aseq_dict["all_api_names"])
                percentage_denominator[1] += 1
            elif 10 < len(aseq_dict["all_api_names"]) <= 15:
                if bseq_dict["WFWorkflowActionIdentifier"] not in aseq_dict["all_api_names"]:
                    hall_numerator[2] += 1
                else:
                    chose_pos = aseq_dict["all_api_names"].index(bseq_dict["WFWorkflowActionIdentifier"])
                    percentage_numerator[2] += chose_pos / len(aseq_dict["all_api_names"])
                percentage_denominator[2] += 1
            elif 15 < len(aseq_dict["all_api_names"]) <= 20:
                if bseq_dict["WFWorkflowActionIdentifier"] not in aseq_dict["all_api_names"]:
                    hall_numerator[3] += 1
                else:
                    chose_pos = aseq_dict["all_api_names"].index(bseq_dict["WFWorkflowActionIdentifier"])
                    percentage_numerator[3] += chose_pos / len(aseq_dict["all_api_names"])
                percentage_denominator[3] += 1
            else:
                if bseq_dict["WFWorkflowActionIdentifier"] not in aseq_dict["all_api_names"]:
                    hall_numerator[4] += 1
                else:
                    chose_pos = aseq_dict["all_api_names"].index(bseq_dict["WFWorkflowActionIdentifier"])
                    percentage_numerator[4] += chose_pos / len(aseq_dict["all_api_names"])
                percentage_denominator[4] += 1
                    
        if aseq_dict["len_aseq"] <= 1:
            all_num_list[0] += 1
        elif 1 < aseq_dict["len_aseq"] <= 5:
            all_num_list[1] += 1
            if 'pos' in aseq_dict:
                all_num_every_len_level2[aseq_dict["pos"]] = all_num_every_len_level2.get(aseq_dict["pos"], 0) + 1
        elif 5 < aseq_dict["len_aseq"] <= 15:
            all_num_list[2] += 1
            if 'pos' in aseq_dict:
                all_num_every_len_level3[aseq_dict["pos"]] = all_num_every_len_level3.get(aseq_dict["pos"], 0) + 1
        elif 15 < aseq_dict["len_aseq"] <= 30:
            all_num_list[3] += 1
            if 'pos' in aseq_dict:
                all_num_every_len_level4[aseq_dict["pos"]] = all_num_every_len_level4.get(aseq_dict["pos"], 0) + 1
        
        if len(aseq_dict["all_api_names"]) <= 5:
            all_num_api_nums[0] += 1
        elif 5 < len(aseq_dict["all_api_names"]) <= 10:
            all_num_api_nums[1] += 1
        elif 10 < len(aseq_dict["all_api_names"]) <= 15:
            all_num_api_nums[2] += 1
        elif 15 < len(aseq_dict["all_api_names"]) <= 20:
            all_num_api_nums[3] += 1
        else:
            all_num_api_nums[4] += 1
        
        all_num += 1

        if URL in generated_success_categories:
            category = generated_success_categories[URL]['category']
            if category in categorie2num_dict:
                categories_all_num[categorie2num_dict[category]] += 1

    if print_or_not:
        accuracy = correct_num / all_num
        print(f"Overall accuracy: {correct_num} / {all_num} = {accuracy * 100:.2f}")
        for i, correct_num in enumerate(correct_num_list):
            print(f"Length within the interval{i + 1}的准确率：{correct_num} / {all_num_list[i]} = {correct_num / all_num_list[i] * 100:.2f}")

    return correct_num, all_num, correct_num_list, all_num_list, categories_correct_num, categories_all_num, \
        correct_num_every_len_level2, all_num_every_len_level2, \
        correct_num_every_len_level3, all_num_every_len_level3, \
        correct_num_every_len_level4, all_num_every_len_level4, \
        correct_num_api_nums, all_num_api_nums, \
        hall_numerator, percentage_numerator, percentage_denominator


def judge_if_equal(value1, value2):
    """Determine if two numbers are equal."""

    if isinstance(value1, bool):
        value1 = int(value1)
    if isinstance(value2, bool):
        value2 = int(value2)

    # Only integer, float, and string types remain.
    # If one number is a float, attempt to convert the other number to a float for comparison.
    if isinstance(value1, float) or isinstance(value2, float):
        try:
            value1 = float(value1)
            value2 = float(value2)
        except:
            return False

    # Only integer, float, and string types remain.
    # If one number is an integer, attempt to convert the other number to an integer for comparison. If the conversion fails, convert both numbers to strings and compare them.
    if isinstance(value1, int) or isinstance(value2, int):
        try:
            value1 = int(value1)
            value2 = int(value2)
        except:
            value1 = str(value1)
            value2 = str(value2)

    return value1 == value2


def evaluate_experiment2_basic_para(
    shortcuts_list,
    all_shortcuts_paras_that_is_necessary_in_query,
    check_intersection_of_query_and_para_necessary,
    print_or_not = True,
):
    """Evaluation of Question 2: Verify if the basic parameters are correctly populated.

    Each element of `shortcuts_list` is a dictionary: {
        "URL": URL,
        "query": log_query,
        "api_names": log_api_names,
        "api_descs": log_api_descs,
        "aseqs": aseqs,
        "bseqs": bseqs,
        "cur_input_token_count": cur_input_token_count,
        "cur_output_token_count": cur_output_token_count,
        "cur_input_cost": cur_input_cost,
        "cur_output_cost": cur_output_cost,
        "cur_total_cost": cur_total_cost
    }
    """

    all_shortcuts_paras_that_is_necessary_in_query
    """"https://www.icloud.com/shortcuts/e6fa8dd9e012484bb85c9967f0b83f02": {
        "1": {
            "WFURLActionURL": "https://experience.regmovies.com/unlimited"
        }
    },
    """

    check_intersection_of_query_and_para_necessary
    """
    "https://www.icloud.com/shortcuts/87cd41f5c4694a248fab11085214d04e": {
        "query": "I would like to rename the icon of an app using the App Store search term '提供的输入'. Please use 'App更改图标名称（重写版）V1.0 by SKY 修复：无法制作多个图标，优化用户ti yan' as the text, and prompt me with the message '输入要更改名称图标的app' to input the app name. After selecting the app from the list, continue by prompting me with '选择选择一个app' to choose the proper app from the App Store. After that, set the id and continue the process, making sure to ask me for the description file name with the prompt '请输入描述文件的名称：', the app name with the prompt '请输入App的名称：', and the description file remark with the prompt '描述文件备注'. Also, base64 encode the selected photos every 76 characters, get a UID from 'https://1024tools.com/uuid', and ensure you set the name of the final file as 'Label.mobileconfig'. Finally, open the generated URL.",
        "api_desc": "is.workflow.actions.base64encode(WFEncodeMode: Enum = \"Encode\", WFBase64LineBreakMode: Enum = \"Every 76 Characters\", WFInput: WFVariablePickerParameter(Object)) -> Base64 Encoded: (WFStringContentItem(Object) or public.data(Object))\nParameters:\n    WFEncodeMode:  Mode. The value of this Enum must be one of the following values (The text in parentheses describes the value): \"Encode\", \"Decode\".\n    WFBase64LineBreakMode:  Line Breaks. The value of this Enum must be one of the following values (The text in parentheses describes the value): \"None\", \"Every 64 Characters\", \"Every 76 Characters\". This value depends on the value of WFEncodeMode. This parameter is only valid when the value of \"WFEncodeMode\" is \"Encode\".\n    WFInput:  Input.\nReturn Value:\n    Base64 Encoded: \nDescription:\n    Base64 Encode: Encodes or decodes text or files using Base64 encoding.\nParameterSummary: ${WFEncodeMode} ${WFInput} with base64\n",
        "necessary_paras": {
            "29": {
                "WFHTTPBodyType": "Form",
                "WFHTTPMethod": "POST"
            },
            "34": {
                "WFBase64LineBreakMode": "Every 76 Characters"
            }
        },
        "significant_paras": {
            "29": {
                "WFHTTPBodyType": {
                    "WFHTTPBodyType": "Essential parameter",
                    "reason": "The user explicitly mentioned the need to prompt for the description file name, app name, and description file remark, which indicates the necessity of setting the HTTP body type as 'Form' to handle form values."
                },
                "WFHTTPMethod": {
                    "WFHTTPMethod": "Essential parameter",
                    "reason": "The user specified the usage of the App Store search term, which involves selecting and downloading content, implying the need for an HTTP method like 'POST' to interact with the server."
                }
            },
            "34": {
                "WFBase64LineBreakMode": {
                    "WFBase64LineBreakMode": "Essential parameter",
                    "reason": "The WFBase64LineBreakMode parameter is explicitly mentioned in the user query as part of the required actions."
                }
            }
        }
    """

    """Correct only if both the API prediction and parameter population are accurate."""
    if print_or_not:
        print("Begin evaluating Experiment 2: focus solely on whether the basic parameters are correctly populated.")

    aseq_res_list = []
    bseq_res_list = []

    for cur_shortcut_dict in shortcuts_list:
        URL = cur_shortcut_dict["URL"]
        aseqs = cur_shortcut_dict["aseqs"]
        aseq_len = cal_WFWorkflowActions_len(aseqs, URL)
        bseqs = cur_shortcut_dict["bseqs"]

        for pos, (aseq, bseq) in enumerate(zip(aseqs, bseqs)):  # Ensure that `pos` corresponds to the position in the original shortcut.
            WFWorkflowActionIdentifier = aseq["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters = aseq["WFWorkflowActionParameters"]
            if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                continue
            if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                continue

            aseq_res_list.append({
                "URL": URL,
                "pos": pos,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                "WFWorkflowActionParameters": WFWorkflowActionParameters,
                "len_aseq": aseq_len
            })

            if bseq["state"] == "json_error":
                bseq_res_list.append({
                    "URL": URL,
                    "pos": pos,
                    "WFWorkflowActionIdentifier": None,
                    "WFWorkflowActionParameters": None,
                    "len_aseq": aseq_len
                })
                continue
            elif bseq["state"] == "generated_by_agent" and ("WFWorkflowActionIdentifier" not in bseq["aseq"] or "WFWorkflowActionParameters" not in bseq["aseq"]):
                if "WFWorkflowActionIdentifier" not in bseq["aseq"] and "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "pos": pos,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionIdentifier" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "pos": pos,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": bseq["aseq"]["WFWorkflowActionParameters"],
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "pos": pos,
                        "WFWorkflowActionIdentifier": bseq["aseq"]["WFWorkflowActionIdentifier"],
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                continue

            WFWorkflowActionIdentifier_pred = bseq["aseq"]["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters_pred = bseq["aseq"]["WFWorkflowActionParameters"]
            bseq_res_list.append({
                "URL": URL,
                "pos": pos,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier_pred,
                "WFWorkflowActionParameters": WFWorkflowActionParameters_pred,
                "len_aseq": aseq_len
            })

    # Calculate the overall basic parameter accuracy for `aseq_res_list` and `bseq_res_list`, as well as the accuracy within each of the four interval ranges.
    # The denominator for this calculation is the count of all `significant_paras` with type "Essential parameter" in `check_intersection_of_query_and_para_necessary`.
    para_correct_num, para_all_num = 0, 0
    para_correct_num_list = [0, 0, 0, 0]
    para_all_num_list = [0, 0, 0, 0]
    for aseq_dict, bseq_dict in zip(aseq_res_list, bseq_res_list):
        URL = aseq_dict["URL"]
        pos = aseq_dict["pos"]
        len_aseq = aseq_dict["len_aseq"]
        WFWorkflowActionIdentifier = aseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters = aseq_dict["WFWorkflowActionParameters"]
        WFWorkflowActionIdentifier_pred = bseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters_pred = bseq_dict["WFWorkflowActionParameters"]

        if WFWorkflowActionIdentifier == WFWorkflowActionIdentifier_pred:  # Calculate accuracy based only on the correct parameter population for predictions.
            for para_name, para_value in WFWorkflowActionParameters.items():  # Iterate through all parameters of the current action.
                if URL in check_intersection_of_query_and_para_necessary and str(pos) in check_intersection_of_query_and_para_necessary[URL]["significant_paras"]:
                    necessary_paras_dict = check_intersection_of_query_and_para_necessary[URL]["significant_paras"][str(
                        pos)]
                    # Only parameters marked as "Essential parameter" are considered correct.
                    if para_name in necessary_paras_dict and necessary_paras_dict[para_name][para_name] == "Essential parameter":
                        para_all_num += 1
                        if len_aseq <= 1:
                            para_all_num_list[0] += 1
                        elif 1 < len_aseq <= 5:
                            para_all_num_list[1] += 1
                        elif 5 < len_aseq <= 15:
                            para_all_num_list[2] += 1
                        elif 15 < len_aseq <= 30:
                            para_all_num_list[3] += 1

                        if WFWorkflowActionParameters_pred == None:
                            continue
                        if para_name in WFWorkflowActionParameters_pred and judge_if_equal(para_value, WFWorkflowActionParameters_pred[para_name]):
                            para_correct_num += 1
                            if len_aseq <= 1:
                                para_correct_num_list[0] += 1
                            elif 1 < len_aseq <= 5:
                                para_correct_num_list[1] += 1
                            elif 5 < len_aseq <= 15:
                                para_correct_num_list[2] += 1
                            elif 15 < len_aseq <= 30:
                                para_correct_num_list[3] += 1

    if print_or_not:
        accuracy = para_correct_num / para_all_num
        print(f"Overall basic parameter accuracy: {para_correct_num} / {para_all_num} = {accuracy * 100:.2f}")
        for i, correct_num in enumerate(para_correct_num_list):
            if para_all_num_list[i] != 0:
                print(f"Basic parameter accuracy for lengths within interval {i + 1}: {correct_num} / {
                    para_all_num_list[i]} = {correct_num / para_all_num_list[i] * 100:.2f}")
            else:
                print(f"Basic parameter accuracy for lengths within interval {i + 1}: Denominator value is 0.")

    return para_correct_num, para_all_num, para_correct_num_list, para_all_num_list

def is_return_value_type(value):
    """Determine if a number is in the form of a return value or a system input, i.e., if the value is a dictionary."""

    if not isinstance(value, dict):
        return 0

    if "Value" not in value:
        return 0

    Value = value["Value"]
    if isinstance(Value, dict):
        if "Type" in Value and Value["Type"] == "ActionOutput":
            return 1
        if "Type" in Value and Value["Type"] in ["ExtensionInput"]:
            return 2
        elif "Type" in Value and Value["Type"] in ["CurrentDate"]:
            return 3
        elif "Type" in Value and Value["Type"] in ["Clipboard"]:
            return 4
        elif "Type" in Value and Value["Type"] in ["DeviceDetails"]:
            return 5
        elif "Type" in Value and Value["Type"] in ["Ask"]:
            return 6

    return 0


def judge_if_return_value_equal(value1, value2):
    """Determine if two return values are equal."""

    # If the data types are different, return `False` immediately.
    if not isinstance(value1, dict) or not isinstance(value2, dict):
        return False, 'format_error'

    if "Value" not in value1 or "Value" not in value2:
        return False, 'format_error'

    Value1 = value1["Value"]
    Value2 = value2["Value"]

    if not isinstance(Value1, dict) or not isinstance(Value2, dict):
        return False, 'format_error'

    if "Type" in Value1 and "Type" in Value2 and Value1["Type"] == Value2["Type"]:
        if Value1["Type"] == "ActionOutput":
            UUID_Value1, UUID_Value2 = None, None
            OutputName_Value1, OutputName_Value2 = None, None
            if "OutputUUID" in Value1:
                UUID_Value1 = Value1["OutputUUID"]
            if "OutputUUID" in Value2:
                UUID_Value2 = Value2["OutputUUID"]
            if "OutputName" in Value1:
                OutputName_Value1 = Value1["OutputName"]
            if "OutputName" in Value2:
                OutputName_Value2 = Value2["OutputName"]
            
            if UUID_Value1 and UUID_Value2 and OutputName_Value1 and OutputName_Value2:
                if UUID_Value1 == UUID_Value2 or OutputName_Value1 == OutputName_Value2:
                    return True, None
                else:
                    return False, 'value_error' # The provided value is incorrect.
            elif UUID_Value1 and UUID_Value2:
                if UUID_Value1 == UUID_Value2:
                    return True, None
                else:
                    return False, 'value_error' # The provided value is incorrect.
            elif OutputName_Value1 and OutputName_Value2:
                if OutputName_Value1 == OutputName_Value2:
                    return True, None
                else:
                    return False, 'value_error' # The provided value is incorrect.
            return False, 'value_error' # No value provided.

        if Value1["Type"] in ["ExtensionInput", "CurrentDate", "Clipboard", "DeviceDetails", "Ask"]:
            return True, None
    else:
        return False, 'format_error'

    return False, 'format_error'

def cal_return_para_pos(shortcuts_list):
    """When an action uses the output of a previous action, I want to know the position of the referenced action.
    """
    para_pos = {}
    for cur_shortcut_dict in shortcuts_list:
        URL = cur_shortcut_dict["URL"]
        aseqs = cur_shortcut_dict["aseqs"]
        for aseq in aseqs:
            WFWorkflowActionIdentifier = aseq["WFWorkflowActionIdentifier"]
            if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                continue
            if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                continue
            WFWorkflowActionParameters = aseq["WFWorkflowActionParameters"]
            for para_name, para_value in WFWorkflowActionParameters.items():
                pass


def evaluate_experiment2_return_para(
        shortcuts_list, print_or_not = True):
    """Evaluation of Question 2: Check if the basic parameters are correctly populated.

    Each element of `shortcuts_list` is a dictionary: {
        "URL": URL,
        "query": log_query,
        "api_names": log_api_names,
        "api_descs": log_api_descs,
        "aseqs": aseqs,
        "bseqs": bseqs,
        "cur_input_token_count": cur_input_token_count,
        "cur_output_token_count": cur_output_token_count,
        "cur_input_cost": cur_input_cost,
        "cur_output_cost": cur_output_cost,
        "cur_total_cost": cur_total_cost
    }
    """

    aseq_res_list = []
    bseq_res_list = []

    for cur_shortcut_dict in shortcuts_list:
        URL = cur_shortcut_dict["URL"]
        aseqs = cur_shortcut_dict["aseqs"]
        aseq_len = cal_WFWorkflowActions_len(aseqs, URL)
        bseqs = cur_shortcut_dict["bseqs"]

        for pos, (aseq, bseq) in enumerate(zip(aseqs, bseqs)):
            WFWorkflowActionIdentifier = aseq["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters = aseq["WFWorkflowActionParameters"]
            if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                continue
            if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                continue

            aseq_res_list.append({
                "URL": URL,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                "WFWorkflowActionParameters": WFWorkflowActionParameters,
                "len_aseq": aseq_len
            })

            if bseq["state"] == "json_error":
                bseq_res_list.append({
                    "URL": URL,
                    "WFWorkflowActionIdentifier": None,
                    "WFWorkflowActionParameters": None,
                    "len_aseq": aseq_len
                })
                continue
            elif bseq["state"] == "generated_by_agent" and ("WFWorkflowActionIdentifier" not in bseq["aseq"] or "WFWorkflowActionParameters" not in bseq["aseq"]):
                if "WFWorkflowActionIdentifier" not in bseq["aseq"] and "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionIdentifier" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": bseq["aseq"]["WFWorkflowActionParameters"],
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": bseq["aseq"]["WFWorkflowActionIdentifier"],
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                continue

            WFWorkflowActionIdentifier_pred = bseq["aseq"]["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters_pred = bseq["aseq"]["WFWorkflowActionParameters"]
            bseq_res_list.append({
                "URL": URL,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier_pred,
                "WFWorkflowActionParameters": WFWorkflowActionParameters_pred,
                "len_aseq": aseq_len
            })

    # Calculate the overall accuracy of return value parameter population for `aseq_res_list` and `bseq_res_list`, as well as the accuracy within each of the four interval ranges.
    return_para_correct_num, return_para_all_num = 0, 0
    return_para_correct_num_list = [0, 0, 0, 0]
    return_para_all_num_list = [0, 0, 0, 0]
    return_para_nopred_num_list = [0, 0, 0, 0] # Number of parameters with no predictions.
    return_para_formaterror_num_list = [0, 0, 0, 0] # Parameters with the correct names but incorrect types or formats.
    return_para_chooseerror_num_list = [0, 0, 0, 0] # Parameters with the correct names but incorrect selected values.
    for aseq_dict, bseq_dict in zip(aseq_res_list, bseq_res_list):
        URL = aseq_dict["URL"]
        len_aseq = aseq_dict["len_aseq"]
        WFWorkflowActionIdentifier = aseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters = aseq_dict["WFWorkflowActionParameters"]
        WFWorkflowActionIdentifier_pred = bseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters_pred = bseq_dict["WFWorkflowActionParameters"]

        if WFWorkflowActionIdentifier == WFWorkflowActionIdentifier_pred:
            """If the parameter was not predicted, it counts as incorrect. If it was predicted but incorrect, it also counts as incorrect."""
            for para_name, para_value in WFWorkflowActionParameters.items():
                if is_return_value_type(para_value) == 1:
                    return_para_all_num += 1
                    if len_aseq <= 1:
                        return_para_all_num_list[0] += 1
                    elif 1 < len_aseq <= 5:
                        return_para_all_num_list[1] += 1
                    elif 5 < len_aseq <= 15:
                        return_para_all_num_list[2] += 1
                    elif 15 < len_aseq <= 30:
                        return_para_all_num_list[3] += 1
                    
                    if WFWorkflowActionParameters_pred == None or para_name not in WFWorkflowActionParameters_pred:
                        if len_aseq <= 1:
                            return_para_nopred_num_list[0] += 1
                        elif 1 < len_aseq <= 5:
                            return_para_nopred_num_list[1] += 1
                        elif 5 < len_aseq <= 15:
                            return_para_nopred_num_list[2] += 1
                        elif 15 < len_aseq <= 30:
                            return_para_nopred_num_list[3] += 1
                        continue

                    equal_or_not, error_reason = judge_if_return_value_equal(para_value, WFWorkflowActionParameters_pred[para_name])
                    if equal_or_not:
                        return_para_correct_num += 1
                        if len_aseq <= 1:
                            return_para_correct_num_list[0] += 1
                        elif 1 < len_aseq <= 5:
                            return_para_correct_num_list[1] += 1
                        elif 5 < len_aseq <= 15:
                            return_para_correct_num_list[2] += 1
                        elif 15 < len_aseq <= 30:
                            return_para_correct_num_list[3] += 1
                    else:
                        if error_reason == 'format_error':
                            if len_aseq <= 1:
                                return_para_formaterror_num_list[0] += 1
                            elif 1 < len_aseq <= 5:
                                return_para_formaterror_num_list[1] += 1
                            elif 5 < len_aseq <= 15:
                                return_para_formaterror_num_list[2] += 1
                            elif 15 < len_aseq <= 30:
                                return_para_formaterror_num_list[3] += 1
                        elif error_reason == 'value_error':
                            if len_aseq <= 1:
                                return_para_chooseerror_num_list[0] += 1
                            elif 1 < len_aseq <= 5:
                                return_para_chooseerror_num_list[1] += 1
                            elif 5 < len_aseq <= 15:
                                return_para_chooseerror_num_list[2] += 1
                            elif 15 < len_aseq <= 30:
                                return_para_chooseerror_num_list[3] += 1
                        else:
                            raise Exception("error_reason error")

    if print_or_not:
        accuracy = return_para_correct_num / return_para_all_num
        print(f"Overall return value parameter accuracy: {accuracy * 100:.2f}")
        for i, correct_num in enumerate(return_para_correct_num_list):
            if return_para_all_num_list[i] != 0:
                print(f"Return value parameter accuracy for lengths within interval {i + 1}: {correct_num} / {return_para_all_num_list[i]} = {
                    correct_num / return_para_all_num_list[i] * 100:.2f}")
            else:
                print(f"Basic parameter accuracy for lengths within interval {i + 1}: Denominator value is 0.")

    return return_para_correct_num, return_para_all_num, return_para_correct_num_list, return_para_all_num_list, \
        return_para_nopred_num_list, return_para_formaterror_num_list, return_para_chooseerror_num_list

def evaluate_experiment3(shortcuts_list, print_or_not = True):

    aseq_res_list = []
    bseq_res_list = []

    for cur_shortcut_dict in shortcuts_list:
        URL = cur_shortcut_dict["URL"]
        aseqs = cur_shortcut_dict["aseqs"]
        aseq_len = cal_WFWorkflowActions_len(aseqs, URL)
        bseqs = cur_shortcut_dict["bseqs"]

        for pos, (aseq, bseq) in enumerate(zip(aseqs, bseqs)):
            WFWorkflowActionIdentifier = aseq["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters = aseq["WFWorkflowActionParameters"]
            if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                continue
            if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                continue

            aseq_res_list.append({
                "URL": URL,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                "WFWorkflowActionParameters": WFWorkflowActionParameters,
                "len_aseq": aseq_len
            })

            if bseq["state"] == "json_error":
                bseq_res_list.append({
                    "URL": URL,
                    "WFWorkflowActionIdentifier": None,
                    "WFWorkflowActionParameters": None,
                    "len_aseq": aseq_len
                })
                continue
            elif bseq["state"] == "generated_by_agent" and ("WFWorkflowActionIdentifier" not in bseq["aseq"] or "WFWorkflowActionParameters" not in bseq["aseq"]):
                if "WFWorkflowActionIdentifier" not in bseq["aseq"] and "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionIdentifier" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": None,
                        "WFWorkflowActionParameters": bseq["aseq"]["WFWorkflowActionParameters"],
                        "len_aseq": aseq_len
                    })
                elif "WFWorkflowActionParameters" not in bseq["aseq"]:
                    bseq_res_list.append({
                        "URL": URL,
                        "WFWorkflowActionIdentifier": bseq["aseq"]["WFWorkflowActionIdentifier"],
                        "WFWorkflowActionParameters": None,
                        "len_aseq": aseq_len
                    })
                continue

            WFWorkflowActionIdentifier_pred = bseq["aseq"]["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters_pred = bseq["aseq"]["WFWorkflowActionParameters"]
            bseq_res_list.append({
                "URL": URL,
                "WFWorkflowActionIdentifier": WFWorkflowActionIdentifier_pred,
                "WFWorkflowActionParameters": WFWorkflowActionParameters_pred,
                "len_aseq": aseq_len
            })

    system_para_correct_num, system_para_all_num = 0, 0
    system_para_correct_num_list = [0, 0, 0, 0]
    system_para_all_num_list = [0, 0, 0, 0]

    system_para_ExtensionInput_num, system_para_CurrentDate_num, system_para_Clipboard_num, system_para_DeviceDetails_num, system_para_Ask_num = 0, 0, 0, 0, 0
    system_para_ExtensionInput_correct_num, system_para_CurrentDate_correct_num, system_para_Clipboard_correct_num, system_para_DeviceDetails_correct_num, system_para_Ask_correct_num = 0, 0, 0, 0, 0
    for aseq_dict, bseq_dict in zip(aseq_res_list, bseq_res_list):
        URL = aseq_dict["URL"]
        len_aseq = aseq_dict["len_aseq"]
        WFWorkflowActionIdentifier = aseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters = aseq_dict["WFWorkflowActionParameters"]
        WFWorkflowActionIdentifier_pred = bseq_dict["WFWorkflowActionIdentifier"]
        WFWorkflowActionParameters_pred = bseq_dict["WFWorkflowActionParameters"]

        if WFWorkflowActionIdentifier == WFWorkflowActionIdentifier_pred:
            for para_name, para_value in WFWorkflowActionParameters.items():
                return_value_type = is_return_value_type(para_value)
                if return_value_type in [2, 3, 4, 5, 6]:
                    system_para_all_num += 1
                    if len_aseq <= 1:
                        system_para_all_num_list[0] += 1
                    elif 1 < len_aseq <= 5:
                        system_para_all_num_list[1] += 1
                    elif 5 < len_aseq <= 15:
                        system_para_all_num_list[2] += 1
                    elif 15 < len_aseq <= 30:
                        system_para_all_num_list[3] += 1
                    
                    if return_value_type == 2:
                        system_para_ExtensionInput_num += 1
                    elif return_value_type == 3:
                        system_para_CurrentDate_num += 1
                    elif return_value_type == 4:
                        system_para_Clipboard_num += 1
                    elif return_value_type == 5:
                        system_para_DeviceDetails_num += 1
                    elif return_value_type == 6:
                        system_para_Ask_num += 1

                    if WFWorkflowActionParameters_pred == None or para_name not in WFWorkflowActionParameters_pred:
                        continue

                    equal_or_not, error_reason = judge_if_return_value_equal(para_value, WFWorkflowActionParameters_pred[para_name])

                    if equal_or_not:
                        system_para_correct_num += 1
                        if len_aseq <= 1:
                            system_para_correct_num_list[0] += 1
                        elif 1 < len_aseq <= 5:
                            system_para_correct_num_list[1] += 1
                        elif 5 < len_aseq <= 15:
                            system_para_correct_num_list[2] += 1
                        elif 15 < len_aseq <= 30:
                            system_para_correct_num_list[3] += 1
                        
                        if return_value_type == 2:
                            system_para_ExtensionInput_correct_num += 1
                        elif return_value_type == 3:
                            system_para_CurrentDate_correct_num += 1
                        elif return_value_type == 4:
                            system_para_Clipboard_correct_num += 1
                        elif return_value_type == 5:
                            system_para_DeviceDetails_correct_num += 1
                        elif return_value_type == 6:
                            system_para_Ask_correct_num += 1

    if print_or_not:
        system_accuracy = system_para_correct_num / system_para_all_num
        print(f"Overall system parameter accuracy: {system_accuracy * 100:.2f}")
        for i, correct_num in enumerate(system_para_correct_num_list):
            if system_para_all_num_list[i] != 0:
                print(f"System parameter accuracy for lengths within interval {i + 1}: {correct_num} / {system_para_all_num_list[i]} = {
                    correct_num / system_para_all_num_list[i] * 100:.2f}")
            else:
                print(f"Basic parameter accuracy for lengths within interval {i + 1}: Denominator value is 0.")
    
    return system_para_correct_num, system_para_all_num, system_para_correct_num_list, system_para_all_num_list, \
        system_para_ExtensionInput_num, system_para_CurrentDate_num, system_para_Clipboard_num, system_para_DeviceDetails_num, system_para_Ask_num, system_para_ExtensionInput_correct_num, system_para_CurrentDate_correct_num, system_para_Clipboard_correct_num, system_para_DeviceDetails_correct_num, system_para_Ask_correct_num


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--evaluate_instead_of_generate",
                        action="store_true")  # Calculate the evaluation metrics for the existing results, rather than generating new results.
    argparser.add_argument("--model_name", type=str,
                        default=None)  # Model name
    argparser.add_argument("--sample_num", type=int,
                        default=0)
    args = argparser.parse_args()

    if args.model_name:
        MODEL_NAME = args.model_name
    else:
        raise NotImplementedError

    use_openai_style = False  # Use OpenAI's style
    use_google_style = False  # Use Google's style
    use_dashscope_style = False  # Use DashScope's style
    call_num = 0

    if MODEL_NAME in [
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0.9,
            "top_p": 1}
        use_google_style = True
        model = genai.GenerativeModel(model_name = MODEL_NAME)

        if MODEL_NAME == "gemini-1.5-pro":
            input_price_every_million, output_price_every_million = 3.5, 7. # $3.50 for 1,000,000 inputs, $7.00 for 1,000,000 outputs
        elif MODEL_NAME == "gemini-1.5-flash":
            input_price_every_million, output_price_every_million = 0.35, 1.05 # $3.50 for 1,000,000 inputs, $7.00 for 1,000,000 outputs

    elif MODEL_NAME in [
        "gpt-3.5-turbo",
    ]:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = openai.OpenAI()
        create_completion_client = client.chat.completions.create
        # gpt-3.5-turbo-0125 Input: $0.50 / 1M tokens, Output: $1.50 / 1M tokens
        input_price_every_million, output_price_every_million = 0.5, 1.5
        use_openai_style = True

    elif MODEL_NAME in [  # Alibaba Cloud Llama3-8b-Instruct
        "llama3-8b-instruct",
        "llama3-70b-instruct",
    ]:

        DASHSCOPE_API_KEYs = [
            os.getenv("DASHSCOPE_API_KEY"),
            os.getenv("DASHSCOPE_API_KEY_1")
        ]

        if MODEL_NAME == "llama3-8b-instruct":
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Limited-time free offer
            use_dashscope_style = True
        elif MODEL_NAME == "llama3-70b-instruct":
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Limited-time free offer
            use_dashscope_style = True
    elif MODEL_NAME in [
        "meta-llama/Llama-3-70b-chat-hf",
        "gpt-4o"
    ]:

        AI_ML_API_KEY = os.getenv("AI_ML_API_KEY")
        client = openai.OpenAI(
            api_key=AI_ML_API_KEY,  # Replace with the actual DashScope API_KEY.
            base_url="https://api.aimlapi.com",  # Enter the DashScope service endpoint.
        )
        create_completion_client = client.chat.completions.create
        input_price_every_million, output_price_every_million = 0., 0. # $5.00 for 10,000,000 tokens
        use_openai_style = True

    elif MODEL_NAME in [
        'qwen2-0.5b-instruct',  # unk
        'qwen2-1.5b-instruct',  # unk
        'qwen2-7b-instruct',  # unk
        'qwen2-57b-a14b-instruct',  # unk
        'qwen2-72b-instruct',  # unk
    ]:
        DASHSCOPE_API_KEYs = [
            os.getenv("DASHSCOPE_API_KEY"),
            os.getenv("DASHSCOPE_API_KEY_1")
        ]

        if MODEL_NAME == 'qwen2-0.5b-instruct':
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.
            use_dashscope_style = True
        elif MODEL_NAME == 'qwen2-1.5b-instruct':
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.
            use_dashscope_style = True
        elif MODEL_NAME == 'qwen2-7b-instruct':
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.
            use_dashscope_style = True
        elif MODEL_NAME == 'qwen2-57b-a14b-instruct':
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.
            use_dashscope_style = True
        elif MODEL_NAME == 'qwen2-72b-instruct':
            create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.
            use_dashscope_style = True

    elif MODEL_NAME in [  # Alibaba Cloud Llama3-8b-Instruct
        'qwen1.5-0.5b-chat',  # unk
        'qwen1.5-1.8b-chat',  # unk
        'qwen1.5-7b-chat',  # 0.001 and 0.002 yuan
        'qwen1.5-14b-chat',  # 0.002, 0.004 yuan
        'qwen1.5-32b-chat',  # 0.0035, 0.007 yuan
        'qwen1.5-72b-chat',  # 0.005, 0.01 yuan
        'qwen1.5-110b-chat',  # 0.006, 0.012 yuan

        "qwen-long",  # 0.0005, 0.002 yuan
        'qwen-turbo',  # 0.002, 0.006 yuan
        "qwen-plus",  # 0.004, 0.012 yuan
        'qwen-max',  # 0.04, 0.12 yuan
        'qwen-max-0107',  # 0.04, 0.12 yuan
        'qwen-max-0403',  # 0.04, 0.12 yuan
        'qwen-max-0428',  # 0.04, 0.12 yuan
        'qwen-max-longcontext',  # 0.04, 0.12 yuan
    ]:
        DASHSCOPE_API_KEYs = [
            os.getenv("DASHSCOPE_API_KEY"),
            os.getenv("DASHSCOPE_API_KEY_1")
        ]
        DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
        client = openai.OpenAI(
            api_key=DASHSCOPE_API_KEY,  # Replace with the actual DashScope API key.
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # Enter the DashScope service endpoint.
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'qwen1.5-0.5b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # unk
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-1.8b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # unk
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-7b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 1, 2  # yuan
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-14b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 2, 4  # yuan
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-32b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 3.5, 7  # yuan
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-72b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 5, 10  # yuan
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen1.5-110b-chat':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 6, 12  # yuan
            # use_dashscope_style = True
        elif MODEL_NAME == "qwen-long":
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0.5, 2
            # use_dashscope_style = True
        elif MODEL_NAME == 'qwen-turbo':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 2, 6
            # use_dashscope_style = True
        elif MODEL_NAME == "qwen-plus":
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 4, 12
            # use_dashscope_style = True
        elif MODEL_NAME in [
            'qwen-max',
            'qwen-max-0107',
            'qwen-max-0403',
            'qwen-max-0428',
            'qwen-max-longcontext',
        ]:
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 40, 120
            # use_dashscope_style = True

    elif MODEL_NAME in [
        'chatglm3-6b',
    ]:
        DASHSCOPE_API_KEYs = [
            os.getenv("DASHSCOPE_API_KEY"),
            os.getenv("DASHSCOPE_API_KEY_1")
        ]
        DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
        client = openai.OpenAI(
            api_key=DASHSCOPE_API_KEY,  # Replace with the actual DashScope API key.
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # Enter the DashScope service endpoint.
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'chatglm3-6b':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Free for a limited time
            # use_dashscope_style = True

    elif MODEL_NAME in [
        'moonshot-v1-8k',
        'moonshot-v1-32k',
    ]:
        DASHSCOPE_API_KEYs = [
            os.getenv("DASHSCOPE_API_KEY"),
            os.getenv("DASHSCOPE_API_KEY_1")
        ]
        DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
        client = openai.OpenAI(
            api_key=DASHSCOPE_API_KEY,  # Replace with the actual DashScope API key.
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # Enter the DashScope service endpoint.
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'moonshot-v1-8k':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Free for a limited time
            # use_dashscope_style = True
        elif MODEL_NAME == 'moonshot-v1-32k':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Free for a limited time
            # use_dashscope_style = True

    elif MODEL_NAME in [
        'baichuan2-turbo',
    ]:

        DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
        client = openai.OpenAI(
            api_key=DASHSCOPE_API_KEY,  # Replace with the actual DashScope API key.
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # Enter the DashScope service endpoint.
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'baichuan2-turbo':
            # create_completion_client = dashscope.Generation.call
            input_price_every_million, output_price_every_million = 0., 0.  # Free for a limited time
            # use_dashscope_style = True

    elif MODEL_NAME in [
        'deepseek-chat',
        'deepseek-coder',
    ]:

        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,  # Replace with the actual DEEPSEEK API key.
            base_url="https://api.deepseek.com",  # Enter the DEEPSEEK service endpoint.
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'deepseek-chat':
            input_price_every_million, output_price_every_million = 0.14, 0.28
        elif MODEL_NAME == 'deepseek-coder':
            input_price_every_million, output_price_every_million = 0.14, 0.28
        pass

    elif MODEL_NAME in [
        'GLM-4-Air'
    ]:
        CHATGLM_API_KEY = os.getenv("CHATGLM_API_KEY")
        client = openai.OpenAI(
            api_key=CHATGLM_API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        create_completion_client = client.chat.completions.create
        use_openai_style = True

        if MODEL_NAME == 'GLM-4-Air':
            input_price_every_million, output_price_every_million = 1, 1

    else:
        raise NotImplementedError

    assert sum([use_openai_style, use_google_style, use_dashscope_style]) == 1

    input_token_count, output_token_count = 0, 0

    if not args.evaluate_instead_of_generate:

        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.INFO)
        if not os.path.exists('log'):
            os.makedirs('log')
        file_handler = logging.FileHandler(
            f'log/6_experiment_{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.log')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        logger.info(f"MODEL_NAME: {MODEL_NAME}")

    all_api2info, all_api2paraname2paratype = get_all_api_info()

    # Retrieve the generated query.
    generated_success_queries_path = os.path.join(
        SHORTCUT_DATA, "generated_success_queries.json")
    with open(generated_success_queries_path, "r") as f:
        generated_success_queries = json.load(f)
    if not args.evaluate_instead_of_generate:
        logger.info(f"已经生成的 query 的个数：{len(generated_success_queries)}")
    # Retrieve all shortcuts.
    final_detailed_records_path = os.path.join(
        SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)
    new_final_detailed_records = {}
    for i, cur_detailed_record in enumerate(final_detailed_records):
        URL = cur_detailed_record["URL"]
        shortcut = cur_detailed_record["shortcut"]
        if shortcut is None:
            continue
        new_final_detailed_records[URL] = cur_detailed_record
    final_detailed_records = new_final_detailed_records
    del new_final_detailed_records
    if not args.evaluate_instead_of_generate:
        logger.info(f"There are a total of {len(final_detailed_records)} shortcuts.")

    """"Mapping from shortcuts to action positions to parameter names"""
    all_shortcuts_paras_that_is_necessary_in_query = get_all_shortcuts_paras_that_is_necessary_in_query(
        list(final_detailed_records.values()), all_api2paraname2paratype)
    check_intersection_of_query_and_para_necessary_path = os.path.join(
        SHORTCUT_DATA, "json-gpt-3.5-turbo_check_intersection_of_query_and_para_necessary.json")
    with open(check_intersection_of_query_and_para_necessary_path, "r") as f:
        check_intersection_of_query_and_para_necessary = json.load(f)
    if not args.evaluate_instead_of_generate:
        logger.info(f"Number of necessary parameters, including `String` type: {len(all_shortcuts_paras_that_is_necessary_in_query)}. Number of shortcuts excluding `String`: {len(check_intersection_of_query_and_para_necessary)}.")

    # Slashes (/) in `MODEL_NAME` will be replaced with underscores (_).
    path_model_name = MODEL_NAME.replace("/", "_")
    res_path = os.path.join(SHORTCUT_DATA, 
                            # Path to store the final agent-generated results
                            "tmp", f"experiment1_res_{path_model_name}.jsonl")
    already_processed_shortcuts_list = []  # Final saved experimental results
    if os.path.exists(res_path):
        with open(res_path, "r") as f:
            already_processed_shortcuts_list = [
                json.loads(line) for line in f.readlines()]
    already_processed_shortcuts_set = set(
        [res["URL"] for res in already_processed_shortcuts_list])  # Processed shortcuts will not be reprocessed.

    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    if args.evaluate_instead_of_generate:
        already_processed_shortcuts_list
        evaluate_experiment1(already_processed_shortcuts_list)

        evaluate_experiment2_basic_para(
            already_processed_shortcuts_list, all_shortcuts_paras_that_is_necessary_in_query, check_intersection_of_query_and_para_necessary)

        evaluate_experiment2_return_para(already_processed_shortcuts_list)

        evaluate_experiment3(already_processed_shortcuts_list)
    else:

        del already_processed_shortcuts_list

        to_be_processed_num = len(
            final_detailed_records) - len(already_processed_shortcuts_set)
        logger.info(f"Number of processed shortcuts: {len(already_processed_shortcuts_set)}. Number of remaining shortcuts: {to_be_processed_num}")
        
        # # Randomly select 200 entries from `generated_success_queries` to create a new dictionary, `random_200_success_queries`.
        # random_200_success_queries = {}
        # random_200_success_queries_URLs = random.sample(
        #     list(generated_success_queries.keys()), args.sample_num)
        # for URL in random_200_success_queries_URLs:
        #     random_200_success_queries[URL] = generated_success_queries[URL]

        # Randomly shuffle `generated_success_queries`.
        generated_success_queries = dict(
            random.sample(list(generated_success_queries.items()), len(generated_success_queries)))

        if args.sample_num:
            sampled_queries = dict(random.sample(list(generated_success_queries.items()), args.sample_num))
            logger.info(f"Sampled {args.sample_num} shortcuts.")
        

        new_shortcuts_list = []  # Store the new experimental results.
        logger.info("Begin processing new shortcuts.")
        cnt = 0  # Number of new shortcuts processed this times
        # for URL, cur_query_dict in random_200_success_queries.items():
        for URL, cur_query_dict in generated_success_queries.items():

            if URL in already_processed_shortcuts_set:  # Shortcuts that have already been processed will not be reprocessed.
                continue

            logger.info(f"Processing {URL}, {
                        cnt}/{to_be_processed_num}= {cnt / to_be_processed_num * 100:.2f}")

            GeneratedQuery = cur_query_dict["GeneratedQuery"]
            shortcut_name = GeneratedQuery["shortcut_name"]
            shortcut_description = GeneratedQuery["shortcut_description"]
            query = GeneratedQuery["query"]
            logger.info(f"The current query is: {query}")

            if URL not in final_detailed_records:
                continue

            cur_detailed_record = final_detailed_records[URL]  # Retrieve detailed information for the current shortcut.
            shortcut = cur_detailed_record["shortcut"]
            WFWorkflowActions = shortcut["WFWorkflowActions"]

            unique_identifies = []  # Retrieve all `WFWorkflowActionIdentifier` for the current shortcut.
            for action in WFWorkflowActions:
                WFWorkflowActionIdentifier = action["WFWorkflowActionIdentifier"]
                if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                    continue
                if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:
                    continue
                unique_identifies.append(WFWorkflowActionIdentifier)
            unique_identifies = list(set(unique_identifies))
            random_multiple = random.randint(3, 5)  # Sample 3 to 5 times the number of APIs.
            extra_API_names = sample_more_APIs(all_api2info, max(min(len(
                unique_identifies) * random_multiple, 20 - len(unique_identifies)), 0), exclude_APIs=unique_identifies)
            input_API_names = unique_identifies + extra_API_names
            # input_API_names = random.shuffle(input_API_names)
            # input_API_names = sorted(input_API_names)
            input_API_descs = {}
            for API_name in input_API_names:
                if API_name in all_api2info:
                    input_API_descs[API_name] = all_api2info[API_name]
                else:
                    input_API_descs[API_name] = "No description available."
            input_API_descs = dict(
                sorted(input_API_descs.items(), key=lambda item: item[0]))

            agent_instance = APIBasedAgent(input_API_descs)

            log_query = query  # One query per shortcut.
            log_api_descs = input_API_descs  # Each shortcut has multiple available APIs, represented as a dictionary mapping API names to API descriptions.
            log_api_names = input_API_names  # Each shortcut has multiple available APIs, represented as a list of API names.
            aseqs = WFWorkflowActions
            identifier2return_value = get_identifier2return_value(
                aseqs, all_api2paraname2paratype)
            tmp_aseqs = []  # Each shortcut has multiple actions, corresponding one-to-one with the standard answers. This list does not include actions from `filter_WFWorkflowActionIdentifier_list`.
            bseqs = []  # Each shortcut has multiple actions, corresponding one-to-one with the standard answers. This list includes actions from `filter_WFWorkflowActionIdentifier_list` and should be stored.
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                all_api_descs=agent_instance.all_api_descs,
                all_api_names=agent_instance.all_api_names,
            )

            cur_input_token_count, cur_output_token_count = 0, 0
            cur_input_cost, cur_output_cost, cur_total_cost = 0, 0, 0

            context_length_exceeded_error = False
            for aseq in aseqs:

                WFWorkflowActionIdentifier = copy.deepcopy(
                    aseq["WFWorkflowActionIdentifier"])
                # Modifications to `WFWorkflowActionParameters` will alter the original `aseqs`, potentially causing errors in the `calc_WFWorkflowActions_len(aseqs)` calculation.
                WFWorkflowActionParameters = copy.deepcopy(
                    aseq["WFWorkflowActionParameters"])

                # For third-party apps, the fields `ShowWhenRun` and `OpenWhenRun` may appear.
                WFWorkflowActionParameters.pop("ShowWhenRun", None)
                WFWorkflowActionParameters.pop("OpenWhenRun", None)
                # For third-party apps, the `AppIntentDescriptor` field may appear.
                WFWorkflowActionParameters.pop("AppIntentDescriptor", None)

                remove_wf_serialization_types(
                    WFWorkflowActionParameters)  # Remove the `WFSerializationType` field.
                # Remove the `WFCoercionVariableAggrandizement`, `WFDateFormatVariableAggrandizement`, and `WFUnitVariableAggrandizement` fields from `Aggrandizements`.
                count_and_clean_aggrandizements(WFWorkflowActionParameters)
                # Replace `￼` in `attachmentsByRange` and sort.
                replace_and_sort_attachments(WFWorkflowActionParameters)

                # If `CustomOutputName` does not exist, use `DefaultOutputName` if available.
                if "UUID" in WFWorkflowActionParameters:
                    UUID = WFWorkflowActionParameters["UUID"]
                    if UUID in identifier2return_value:
                        if "CustomOutputName" not in WFWorkflowActionParameters:
                            if UUID in identifier2return_value:
                                WFWorkflowActionParameters["CustomOutputName"] = identifier2return_value[UUID]

                if "CustomOutputName" in WFWorkflowActionParameters:
                    WFWorkflowActionParameters["OutputName"] = WFWorkflowActionParameters["CustomOutputName"]
                    WFWorkflowActionParameters.pop("CustomOutputName")

                if WFWorkflowActionIdentifier in filter_WFWorkflowActionIdentifier_list:
                    bseqs.append({"state": "copy_from_true",
                                 "aseq": aseq})  # Copy directly from the correct answer.
                    continue

                if WFWorkflowActionIdentifier in ignore_in_judge_WFWorkflowActionIdentifier_list:  # These actions do not require the agent to predict.

                    if WFWorkflowActionIdentifier == "is.workflow.actions.conditional":  # Modify the `if` branches so they are understandable by the agent.
                        # Modify `WFControlFlowMode`
                        if WFWorkflowActionParameters["WFControlFlowMode"] == 0:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "If Begin"
                        elif WFWorkflowActionParameters["WFControlFlowMode"] == 1:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "Else"
                        elif WFWorkflowActionParameters["WFControlFlowMode"] == 2:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "End If"
                        else:
                            raise ValueError(f"WFControlFlowMode {
                                             WFWorkflowActionParameters['WFControlFlowMode']} is not supported.")
                        # Modify `WFCondition`
                        if "WFCondition" in WFWorkflowActionParameters:
                            condition_value = str(
                                WFWorkflowActionParameters["WFCondition"])
                            WFWorkflowActionParameters["WFCondition"] = branch_num_2_nlp_desc.get(
                                condition_value, str(condition_value))
                        tmp_aseqs.append({"WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                                         "WFWorkflowActionParameters": WFWorkflowActionParameters})
                    elif WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":  # Modify the `Case` statements so they are understandable by the agent.
                        # Adjust `WFControlFlowMode`.
                        if WFWorkflowActionParameters["WFControlFlowMode"] == 0:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "Case Begin"
                        elif WFWorkflowActionParameters["WFControlFlowMode"] == 1:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "Case"
                        elif WFWorkflowActionParameters["WFControlFlowMode"] == 2:
                            WFWorkflowActionParameters["WFControlFlowMode"] = "End Case"
                        else:
                            raise ValueError(f"WFControlFlowMode {
                                             WFWorkflowActionParameters['WFControlFlowMode']} is not supported.")
                        tmp_aseqs.append({"WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                                         "WFWorkflowActionParameters": WFWorkflowActionParameters})
                    else:
                        tmp_aseqs.append({"WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                                         "WFWorkflowActionParameters": WFWorkflowActionParameters})

                    bseqs.append({"state": "copy_from_true",
                                 "aseq": aseq})  # Copy directly from the correct answer.

                    continue

                agent_instance.set_history_actions(tmp_aseqs)  # Set historical actions
                user_prompt = USER_PROMPT_TEMPLATE.format(
                    query=query,
                    history_actions=agent_instance.get_history_action_str(),
                )

                try_times = 6
                save_try_times = 5
                cur_try_time = 0

                while cur_try_time < try_times:
                    if use_openai_style:
                        try:
                            completion = create_completion_client(
                                model=MODEL_NAME,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_prompt}
                                ]
                            )

                            cur_input_token_count += completion.usage.prompt_tokens
                            cur_output_token_count += completion.usage.completion_tokens
                            cur_input_cost = cur_input_token_count / 1000000 * input_price_every_million
                            cur_output_cost = cur_output_token_count / 1000000 * output_price_every_million
                            cur_total_cost = cur_input_cost + cur_output_cost

                            input_token_count += completion.usage.prompt_tokens
                            output_token_count += completion.usage.completion_tokens
                            input_cost = input_token_count / 1000000 * input_price_every_million
                            output_cost = output_token_count / 1000000 * output_price_every_million
                            total_cost = input_cost + output_cost

                            break

                        except Exception as e:
                            print(
                                f"Fail! Generation Error! generating action for {URL}")
                            print(e)

                            # If `context_length_exceeded` appears in `str(e)`.
                            if "context_length_exceeded" in str(e):  # chatgpt
                                context_length_exceeded_error = True
                                break
                            elif "maximum context length is" in str(e):  # deepseek
                                context_length_exceeded_error = True
                                break
                            elif "Range of input length should be" in str(e):
                                context_length_exceeded_error = True
                                break
                            elif "Input validation error" in str(e):
                                context_length_exceeded_error = True
                                break
                            elif 'Content Exists Risk' in str(e): # deepseek
                                context_length_exceeded_error = True
                                break
                            elif "Sorry! We've encountered an issue with repetitive patterns in your prompt" in str(e): # openai
                                context_length_exceeded_error = True
                                break
                            elif "encode character" in str(e): # openai
                                context_length_exceeded_error = True
                                break
                            elif "Expected a string with maximum length" in str(e):
                                context_length_exceeded_error = True
                                break
                            elif "The system detects that the input or generated content may contain unsafe or sensitive material." in str(e): # GLM-4-Air
                                context_length_exceeded_error = True
                                break
                            cur_try_time += 1
                            time.sleep(1)

                            if cur_try_time == save_try_times:
                                # Save the current result.
                                print(f"Processed {cnt} results.")
                                path_model_name = MODEL_NAME.replace("/", "_")
                                cost_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_cost_{path_model_name}.jsonl")
                                # with open(cost_path, "a") as f:
                                #     write_str = json.dumps({
                                #         "input_token_count": input_token_count,
                                #         "output_token_count": output_token_count,
                                #         "input_cost": input_cost,
                                #         "output_cost": output_cost,
                                #         "total_cost": total_cost
                                #     }, ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                path_model_name = MODEL_NAME.replace("/", "_")
                                res_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_res_{path_model_name}.jsonl")
                                # with open(res_path, "a") as f:
                                #     write_str = ""
                                #     for res in new_shortcuts_list:
                                #         write_str += json.dumps(res,
                                #                                 ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                new_shortcuts_list = []

                            if cur_try_time >= try_times:
                                raise e
                            
                    elif use_google_style:
                        try:
                            chat = model.start_chat(history=[])
                            completion = chat.send_message("System: " + system_prompt + "\nUser: " + user_prompt)

                            cur_input_token_count += completion.usage_metadata.prompt_token_count
                            cur_output_token_count += completion.usage_metadata.candidates_token_count
                            cur_input_cost = cur_input_token_count / 1000000 * input_price_every_million
                            cur_output_cost = cur_output_token_count / 1000000 * output_price_every_million
                            cur_total_cost = cur_input_cost + cur_output_cost

                            input_token_count += completion.usage_metadata.prompt_token_count
                            output_token_count += completion.usage_metadata.candidates_token_count
                            input_cost = input_token_count / 1000000 * input_price_every_million
                            output_cost = output_token_count / 1000000 * output_price_every_million
                            total_cost = input_cost + output_cost

                            break

                        except Exception as e:
                            print(
                                f"Fail! Generation Error! generating action for {URL}")
                            print(e)

                            # If `context_length_exceeded` appears in `str(e)`.
                            if "context_length_exceeded" in str(e):
                                context_length_exceeded_error = True
                                break
                            if "HARM_CATEGORY_HARASSMENT" in str(e):
                                context_length_exceeded_error = True
                                break
                            if "HARM_CATEGORY_SEXUALLY_EXPLICIT" in str(e):
                                context_length_exceeded_error = True
                                break
                            if "HARM_CATEGORY_DANGEROUS_CONTENT" in str(e):
                                context_length_exceeded_error = True
                                break
                            if "HARM_CATEGORY_HATE_SPEECH" in str(e):
                                context_length_exceeded_error = True
                                break

                            cur_try_time += 1
                            time.sleep(1)

                            if cur_try_time == save_try_times:
                                # Save the current results.

                                print(f"Processed {cnt} results.")

                                path_model_name = MODEL_NAME.replace("/", "_")
                                cost_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_cost_{path_model_name}.jsonl")
                                # with open(cost_path, "a") as f:
                                #     write_str = json.dumps({
                                #         "input_token_count": input_token_count,
                                #         "output_token_count": output_token_count,
                                #         "input_cost": input_cost,
                                #         "output_cost": output_cost,
                                #         "total_cost": total_cost
                                #     }, ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                path_model_name = MODEL_NAME.replace("/", "_")
                                res_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_res_{path_model_name}.jsonl")
                                # with open(res_path, "a") as f:
                                #     write_str = ""
                                #     for res in new_shortcuts_list:
                                #         write_str += json.dumps(res,
                                #                                 ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                new_shortcuts_list = []

                            if cur_try_time >= try_times:
                                raise e

                    elif use_dashscope_style:
                        try:
                            completion = create_completion_client(
                                model=MODEL_NAME,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_prompt}
                                ]
                            )

                            call_num += 1

                            cur_input_token_count += completion["usage"]["input_tokens"]
                            cur_output_token_count += completion["usage"]["output_tokens"]
                            cur_input_cost = cur_input_token_count / 1000000 * input_price_every_million
                            cur_output_cost = cur_output_token_count / 1000000 * output_price_every_million
                            cur_total_cost = cur_input_cost + cur_output_cost

                            input_token_count += completion["usage"]["input_tokens"]
                            output_token_count += completion["usage"]["output_tokens"]
                            input_cost = input_token_count / 1000000 * input_price_every_million
                            output_cost = output_token_count / 1000000 * output_price_every_million
                            total_cost = input_cost + output_cost

                            break

                        except Exception as e:
                            # If you encounter a `'NoneType' object is not subscriptable` error.
                            if isinstance(e, TypeError):
                                message = completion["message"]
                                if 'Allocated quota exceeded, please increase your quota limit.' in message:
                                    print(
                                        "Allocated quota exceeded, please increase your quota limit.")
                                    time.sleep(15)
                                    continue  # Do not count as an error; continue trying.
                                elif 'Access denied.' in message:
                                    print("AccessDenied")
                                    time.sleep(15)
                                    continue
                                elif "Free allocated quota exceeded." in message:
                                    print("Free allocated quota exceeded.")
                                    cur_try_time += 10
                                elif "Range of input length should be" in str(message):
                                    context_length_exceeded_error = True
                                    break
                                elif "Output data may contain inappropriate content" in str(message):
                                    context_length_exceeded_error = True
                                    break
                                elif "Request timed out, please try again later" in message:
                                    print("Request timed out, please try again later")
                                    time.sleep(15)
                                elif "SSLError" in message:
                                    print("SSLError")
                                    time.sleep(15)
                                else:
                                    print("completion:", json.dumps(
                                        completion, indent=4, ensure_ascii=False))
                                    print(e)
                            
                            print(
                                f"Fail! Generation Error! generating action for {URL}")
                            print(e)

                            # If `context_length_exceeded` appears in `str(e)`.
                            if "context_length_exceeded" in str(e):
                                context_length_exceeded_error = True
                                break

                            cur_try_time += 1
                            time.sleep(1)

                            if cur_try_time == save_try_times:
                                # Save the current results.

                                print(f"Processed {cnt} results.")

                                path_model_name = MODEL_NAME.replace("/", "_")
                                cost_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_cost_{path_model_name}.jsonl")
                                # with open(cost_path, "a") as f:
                                #     write_str = json.dumps({
                                #         "input_token_count": input_token_count,
                                #         "output_token_count": output_token_count,
                                #         "input_cost": input_cost,
                                #         "output_cost": output_cost,
                                #         "total_cost": total_cost
                                #     }, ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                path_model_name = MODEL_NAME.replace("/", "_")
                                res_path = os.path.join(
                                    SHORTCUT_DATA, f"experiment1_res_{path_model_name}.jsonl")
                                # with open(res_path, "a") as f:
                                #     write_str = ""
                                #     for res in new_shortcuts_list:
                                #         write_str += json.dumps(res,
                                #                                 ensure_ascii=False) + "\n"
                                #     f.write(write_str)

                                new_shortcuts_list = []

                            if cur_try_time >= try_times:
                                raise e
                    else:
                        raise ValueError("No style is used.")

                if context_length_exceeded_error:
                    break

                generated_content = None
                try:
                    if use_openai_style:
                        generated_content = completion.choices[0].message.content
                        generated_content = match_brackets(generated_content)
                    elif use_google_style:
                        generated_content = list(completion)[0].text
                        generated_content = match_brackets(generated_content)
                    elif use_dashscope_style:
                        generated_content = completion["output"]["text"]
                        generated_content = match_brackets(generated_content)
                    else:
                        raise ValueError("No style is used.")
                    generated_content = json.loads(generated_content)
                except Exception as e:
                    print(f"Fail! Parse Error! generating action for {URL}")
                    print(e)

                    bseqs.append(
                        {"state": "json_error", "aseq": generated_content})
                    tmp_aseqs.append({"WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                                     "WFWorkflowActionParameters": WFWorkflowActionParameters})  # Prepare for the next prediction.
                    print(f"Token count: {input_token_count}, {output_token_count}, Input Cost {
                          input_cost}, {output_cost}, Total Cost {total_cost}")
                    time.sleep(0.5)
                    continue

                bseqs.append({"state": "generated_by_agent",
                             "aseq": generated_content})
                tmp_aseqs.append({"WFWorkflowActionIdentifier": WFWorkflowActionIdentifier,
                                 "WFWorkflowActionParameters": WFWorkflowActionParameters})  # Prepare for the next prediction.

                logger.info(f"Token count: {input_token_count}, {output_token_count}, Input Cost {
                            input_cost}, {output_cost}, Total Cost {total_cost}")

                time.sleep(0.5)

            if len(aseqs) != len(bseqs):
                res_aseqs = aseqs[:len(bseqs)]
            else:
                res_aseqs = aseqs

            new_shortcuts_list.append({
                "URL": URL,
                "query": log_query,
                "api_names": log_api_names,
                "api_descs": log_api_descs,
                "aseqs": res_aseqs,
                "bseqs": bseqs,
                "cur_input_token_count": cur_input_token_count,
                "cur_output_token_count": cur_output_token_count,
                "cur_input_cost": cur_input_cost,
                "cur_output_cost": cur_output_cost,
                "cur_total_cost": cur_total_cost
            })

            cnt += 1
            logger.info(f"Processed {cnt} results.")
            if cnt % 10 == 0:  # Save every 10 entries.

                logger.info(f"Saving {cnt} results.")
                path_model_name = MODEL_NAME.replace("/", "_")
                cost_path = os.path.join(
                    SHORTCUT_DATA, f"experiment1_cost_{path_model_name}.jsonl")
                # with open(cost_path, "a") as f:
                #     write_str = json.dumps({
                #         "input_token_count": input_token_count,
                #         "output_token_count": output_token_count,
                #         "input_cost": input_cost,
                #         "output_cost": output_cost,
                #         "total_cost": total_cost
                #     }, ensure_ascii=False) + "\n"
                #     f.write(write_str)

                path_model_name = MODEL_NAME.replace("/", "_")
                res_path = os.path.join(
                    SHORTCUT_DATA, f"experiment1_res_{path_model_name}.jsonl")
                # with open(res_path, "a") as f:
                #     write_str = ""
                #     for res in new_shortcuts_list:
                #         write_str += json.dumps(res, ensure_ascii=False) + "\n"
                #     f.write(write_str)

                new_shortcuts_list = []
                logger.info(f"Saved {cnt} results.")

        logger.info(f"Finish processing {cnt} results.")

        if new_shortcuts_list:
            
            path_model_name = MODEL_NAME.replace("/", "_")
            cost_path = os.path.join(
                SHORTCUT_DATA, f"experiment1_cost_{path_model_name}.jsonl")

            # with open(cost_path, "a") as f:
            #     write_str = json.dumps({
            #         "input_token_count": input_token_count,
            #         "output_token_count": output_token_count,
            #         "input_cost": input_cost,
            #         "output_cost": output_cost,
            #         "total_cost": total_cost
            #     }, ensure_ascii=False) + "\n"
            #     f.write(write_str)

            path_model_name = MODEL_NAME.replace("/", "_")
            res_path = os.path.join(
                SHORTCUT_DATA, f"experiment1_res_{path_model_name}.jsonl")
            # with open(res_path, "a") as f:
            #     write_str = ""
            #     for res in new_shortcuts_list:
            #         write_str += json.dumps(res, ensure_ascii=False) + "\n"
            #     f.write(write_str)

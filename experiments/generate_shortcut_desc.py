"""Generate a description file for shortcuts with actions of length <= 30.
"""

import json
import os
import re
import copy

from WFActionsClass import WFActionsClass
from APIsClass import APIsClass

branch_num_2_nlp_desc = {
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

def generate_shortcutdesc(
    WFWorkflowActions,
    identifier2return_value,
    all_api2paraname2paratype,
    all_api2parasummary,
    shortcut_paras_that_is_necessary_in_query,
    depth=None,  # Recursive depth
    pre_index=0,  # Starting index of the previous recursion
):
    """Generate a description file for a shortcut."""

    if depth == None:  # Current recursion depth
        depth = 0

    if not WFWorkflowActions:
        return ""

    WFWorkflowActions_str = ""  # The final generated description string

    i = 0
    while i < len(WFWorkflowActions):
        action = WFWorkflowActions[i]
        WFWorkflowActionIdentifier = action["WFWorkflowActionIdentifier"]

        if WFWorkflowActionIdentifier in [
            "is.workflow.actions.conditional",
            "is.workflow.actions.choosefrommenu",
            "is.workflow.actions.repeat.count",
            "is.workflow.actions.repeat.each",
        ]:
            # For if branches, recursively take the maximum length of the if branch as the length of the if branch.
            GroupingIdentifier = action["WFWorkflowActionParameters"]["GroupingIdentifier"]
            WFControlFlowMode = action["WFWorkflowActionParameters"]["WFControlFlowMode"]
            if WFControlFlowMode == 2:
                if WFWorkflowActionIdentifier == "is.workflow.actions.conditional":
                    i += 1
                    continue
                elif WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":
                    i += 1
                    continue
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.count":
                    i += 1
                    continue
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.each":
                    i += 1
                    continue
                else:
                    raise Exception("Unknown branch")
            # Find the last branch with the same GroupingIdentifier.
            branchs = [WFWorkflowActions[i]]
            branchs_pos = [i]
            for j in range(i+1, len(WFWorkflowActions)):
                if "GroupingIdentifier" in WFWorkflowActions[j]["WFWorkflowActionParameters"] and WFWorkflowActions[j]["WFWorkflowActionParameters"]["GroupingIdentifier"] == GroupingIdentifier:
                    branchs.append(WFWorkflowActions[j])
                    branchs_pos.append(j)
                    # Found the final terminating branch.
                    if WFWorkflowActions[j]["WFWorkflowActionParameters"]["WFControlFlowMode"] == 2:
                        break
            if len(branchs) == 1:
                i += 1
                continue
            else:
                WFControlFlowMode, GroupingIdentifier
                # Retrieve the mapping of the current action's API to all its parameter types.
                api2paraname2paratype = all_api2paraname2paratype[WFWorkflowActionIdentifier]
                # Retrieve the mapping of the current action's API to its summary.
                api2parasummary = all_api2parasummary[WFWorkflowActionIdentifier]
                if i + pre_index in shortcut_paras_that_is_necessary_in_query:  # If there are parameters that must be included in the query.
                    act_paras_that_is_necessary_in_query = shortcut_paras_that_is_necessary_in_query[
                        i + pre_index]
                else:
                    act_paras_that_is_necessary_in_query = {}

                if WFWorkflowActionIdentifier == "is.workflow.actions.conditional":
                    branch_beg_pos = branchs_pos[0]
                    WFWorkflowActionParameters = WFWorkflowActions[
                        branch_beg_pos]["WFWorkflowActionParameters"]
                    action_desc = generate_suitable_ParameterSummary(  # Generate a summary description for a single action.
                        WFWorkflowActionIdentifier,
                        WFWorkflowActionParameters,
                        identifier2return_value,
                        api2paraname2paratype,
                        api2parasummary,
                        act_paras_that_is_necessary_in_query
                    )
                    matches = re.finditer(
                        r'\${WFCondition}=([0-9]+|"[^"]*"|\w+)', action_desc)
                    # String used to store the replacement results.
                    replaced_action_desc = action_desc
                    for match in matches:
                        # Extract the matching value (removing any possible quotes).
                        value = match.group(1).strip('"')
                        # Retrieve the corresponding conditional values from the dictionary.
                        condition_value = branch_num_2_nlp_desc.get(value, str(value))
                        # Replace the values in the original string.
                        replaced_action_desc = re.sub(r'\${WFCondition}=' + re.escape(
                            match.group(1)), f'${{WFCondition}}={condition_value}', replaced_action_desc)
                    action_desc = replaced_action_desc
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + action_desc + "\n"
                elif WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":
                    branch_beg_pos = branchs_pos[0]
                    WFWorkflowActionParameters = WFWorkflowActions[
                        branch_beg_pos]["WFWorkflowActionParameters"]
                    action_desc = generate_suitable_ParameterSummary(  # Generate a summary description for a single action.
                        WFWorkflowActionIdentifier,
                        WFWorkflowActionParameters,
                        identifier2return_value,
                        api2paraname2paratype,
                        api2parasummary,
                        act_paras_that_is_necessary_in_query
                    )
                    WFMenuItems = []
                    if "WFMenuItems" in WFWorkflowActionParameters:
                        WFMenuItems = copy.deepcopy(
                            WFWorkflowActionParameters["WFMenuItems"])
                        for j, WFMenuItem in enumerate(WFMenuItems):
                            if isinstance(WFMenuItem, dict):
                                WFItemType = WFMenuItem["WFItemType"]
                                WFValue = WFMenuItem["WFValue"]
                                WFMenuItems[j] = process_dict_Value2(
                                    WFValue, identifier2return_value)

                    action_desc = action_desc.strip()
                    if WFMenuItems:
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc + ' Available Menu Items include "' + \
                            '"."'.join(WFMenuItems) + '"\n'
                    else:
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc + \
                            ". No Available Menu Items.\n"
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.count":
                    branch_beg_pos = branchs_pos[0]
                    WFWorkflowActionParameters = WFWorkflowActions[
                        branch_beg_pos]["WFWorkflowActionParameters"]
                    action_desc = generate_suitable_ParameterSummary(  # Generate a summary description for a single action.
                        WFWorkflowActionIdentifier,
                        WFWorkflowActionParameters,
                        identifier2return_value,
                        api2paraname2paratype,
                        api2parasummary,
                        act_paras_that_is_necessary_in_query
                    )
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + action_desc + 'Times' + ':'
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.each":
                    branch_beg_pos = branchs_pos[0]
                    WFWorkflowActionParameters = WFWorkflowActions[
                        branch_beg_pos]["WFWorkflowActionParameters"]
                    action_desc = generate_suitable_ParameterSummary(  # Generate a summary description for a single action.
                        WFWorkflowActionIdentifier,
                        WFWorkflowActionParameters,
                        identifier2return_value,
                        api2paraname2paratype,
                        api2parasummary,
                        act_paras_that_is_necessary_in_query
                    )
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + action_desc + ':'

                j = 0
                if WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":
                    branchs_pos = branchs_pos[1:]
                for begin_pos, end_pos in zip(branchs_pos[:-1], branchs_pos[1:]):
                    if WFWorkflowActionIdentifier == "is.workflow.actions.conditional":  # else
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + WFWorkflowActionIdentifier + \
                            "; Else:" + "\n"
                    elif WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":
                        if "WFMenuItemTitle" in WFWorkflowActions[begin_pos]["WFWorkflowActionParameters"]:
                            WFMenuItemTitle = WFWorkflowActions[begin_pos][
                                "WFWorkflowActionParameters"]["WFMenuItemTitle"]
                        elif j < len(WFMenuItems):
                            WFMenuItemTitle = WFMenuItems[j]
                        else:
                            WFMenuItemTitle = ""
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + WFWorkflowActionIdentifier + \
                            f'; Case "{WFMenuItemTitle}":' + "\n"

                    sub_str = generate_shortcutdesc(
                        WFWorkflowActions[begin_pos + 1:end_pos],
                        identifier2return_value,
                        all_api2paraname2paratype,
                        all_api2parasummary,
                        shortcut_paras_that_is_necessary_in_query,
                        depth + 1,
                        pre_index + begin_pos + 1,
                    )
                    if sub_str:
                        if sub_str[-1] == "\n":
                            WFWorkflowActions_str += " " * \
                                (4 * depth) + sub_str
                        else:
                            WFWorkflowActions_str += " " * \
                                (4 * depth) + sub_str + "\n"
                    j += 1

                if WFWorkflowActionIdentifier == "is.workflow.actions.conditional":
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + WFWorkflowActionIdentifier + "; End If\n"
                elif WFWorkflowActionIdentifier == "is.workflow.actions.choosefrommenu":
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + WFWorkflowActionIdentifier + "; End Menu\n"
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.count":
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + WFWorkflowActionIdentifier + "; End Repeat\n"
                elif WFWorkflowActionIdentifier == "is.workflow.actions.repeat.each":
                    WFWorkflowActions_str += " " * \
                        (4 * depth) + WFWorkflowActionIdentifier + "; End Repeat\n"

            i = branchs_pos[-1] + 1
        else:
            if WFWorkflowActionIdentifier in [
                "is.workflow.actions.comment",
                "is.workflow.actions.alert"
            ]:
                i += 1
                continue

            WFWorkflowActionParameters = action["WFWorkflowActionParameters"]

            if i + pre_index in shortcut_paras_that_is_necessary_in_query:  # If there are parameters that must be included in the query.
                act_paras_that_is_necessary_in_query = shortcut_paras_that_is_necessary_in_query[
                    i + pre_index]
            else:
                act_paras_that_is_necessary_in_query = {}

            # It is necessary to ensure that the API has corresponding entries in both ParameterSummary and parameter name to parameter type mappings.
            if WFWorkflowActionIdentifier in all_api2paraname2paratype:
                # Retrieve the mapping of the current action's API to all its parameter types.
                api2paraname2paratype = all_api2paraname2paratype[WFWorkflowActionIdentifier]
                # Retrieve the mapping of the current action's API to its summary.
                api2parasummary = all_api2parasummary[WFWorkflowActionIdentifier]

                action_desc = generate_suitable_ParameterSummary(  # Generate a summary description for a single action.
                    WFWorkflowActionIdentifier,
                    WFWorkflowActionParameters,
                    identifier2return_value,
                    api2paraname2paratype,
                    api2parasummary,
                    act_paras_that_is_necessary_in_query
                )
                if action_desc:
                    if action_desc[-1] == "\n":
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc
                    else:
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc + "\n"

            else:
                paraname2paravalue = get_paraname2paravalue(
                    WFWorkflowActionParameters, identifier2return_value)

                para_str = ""
                # In the form of key = value, key = value, ...
                for j, (key, value) in enumerate(paraname2paravalue.items()):
                    if not j:
                        if isinstance(value, str):
                            para_str += key + "=" + f'"{value}"'
                        else:
                            para_str += key + "=" + str(value)
                    else:
                        if isinstance(value, str):
                            para_str += ", " + str(key) + "=" + f'"{value}"'
                        else:
                            para_str += ", " + str(key) + "=" + str(value)
                action_desc = f"Call function {
                    WFWorkflowActionIdentifier}({para_str})."

                if action_desc:
                    if action_desc[-1] == "\n":
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc
                    else:
                        WFWorkflowActions_str += " " * \
                            (4 * depth) + action_desc + "\n"

            i += 1

    return WFWorkflowActions_str


def get_Aggrandizements_name(agg_dict, identifier2return_value):
    """Given a dictionary of type Aggrandizements, return different strings displayed to shortcut developers based on Aggrandizements["Type"].

    WFDictionaryValueVariableAggrandizement
    WFCoercionVariableAggrandizement
    WFDateFormatVariableAggrandizement

    WFPropertyVariableAggrandizement
    WFUnitVariableAggrandizement
    """

    Type = agg_dict["Type"]
    ret_str = None

    if Type == "ActionOutput":
        OutputName = None
        if "OutputName" in agg_dict:
            OutputName = agg_dict["OutputName"]
            ret_str = "${" + OutputName + "}"
        else:
            OutputUUID = agg_dict["OutputUUID"]
            ret_str = identifier2return_value[OutputUUID]
            ret_str = "${" + ret_str + "}"
    elif Type == "Ask":
        ret_str = "${Ask User}"
        if "Prompt" in agg_dict:
            Prompt = agg_dict["Prompt"]
            ret_str += "${Ask User} with prompt " + '"' + Prompt + '"'
    elif Type == "ExtensionInput" or Type == "Input":
        ret_str = "${Ask for ExtensionInput}"
    elif Type == "CurrentDate":
        ret_str = "${Ask for CurrentDate}"
    elif Type == "Clipboard":
        ret_str = "${Ask for Clipboard}"
    elif Type == "DeviceDetails":
        ret_str = "${Ask for DeviceDetails}"
    elif Type == "Variable":
        VariableName = agg_dict["VariableName"]
        ret_str = '${' + VariableName + '}'
    else:
        raise ValueError("Unknown Aggrandizements type.")

    if "Aggrandizements" in agg_dict:
        Aggrandizements = agg_dict["Aggrandizements"]
        for Aggrandizement in Aggrandizements:
            Aggrandizement_Type = Aggrandizement["Type"]

            if Aggrandizement_Type == "WFPropertyVariableAggrandizement":
                PropertyName = Aggrandizement["PropertyName"]
                ret_str += '.${' + PropertyName + '}'
            elif Aggrandizement_Type == "WFDictionaryValueVariableAggrandizement":  # Retrieve the values from the dictionary
                Aggrandizements_DictionaryKey = Aggrandizement["DictionaryKey"]
                ret_str += ".${" + Aggrandizements_DictionaryKey + '}'
            elif Aggrandizement_Type == "WFCoercionVariableAggrandizement":  # Type coercion
                CoercionItemClass = Aggrandizement["CoercionItemClass"]
                ret_str = f"TypeCasting2{CoercionItemClass}(" + ret_str + ")"
            elif Aggrandizement_Type == "WFDateFormatVariableAggrandizement":
                pass
            elif Aggrandizement_Type == "WFUnitVariableAggrandizement":
                WFMeasurementUnitType = Aggrandizement["WFMeasurementUnitType"]
                WFUnitSymbol = Aggrandizement["WFUnitSymbol"]
                ret_str = ret_str + " " + WFUnitSymbol
                pass
            else:
                raise ValueError("Unknown Aggrandizements type.")

    return ret_str


def process_dict_Value2(para_Value, identifier2return_value):

    if "Value" in para_Value and "WFSerializationType" in para_Value:
        Value = para_Value["Value"]

        # Output from previous actions or inputs from the system
        if "Type" in Value and Value["Type"] in ["ActionOutput", "Ask", "ExtensionInput", "CurrentDate", "Clipboard", "DeviceDetails"]:
            # Expressed in string form
            return get_Aggrandizements_name(Value, identifier2return_value)
        elif "string" in Value and "attachmentsByRange" in Value:
            tmp_str = Value["string"]
            matches = [(match.start(), match.end())
                       for match in re.finditer(r'\ufffc', tmp_str)]
            replace_strs = []
            attachmentsByRange_values = list(
                Value["attachmentsByRange"].values())
            for attachmentsByRange_value in attachmentsByRange_values:
                if "Type" in attachmentsByRange_value and attachmentsByRange_value["Type"] in [
                        "ActionOutput", "Ask", "ExtensionInput", "Input", "CurrentDate", "Clipboard", "DeviceDetails"]:
                    replace_strs.append(get_Aggrandizements_name(
                        attachmentsByRange_value, identifier2return_value))
                elif "Type" in attachmentsByRange_value and attachmentsByRange_value["Type"] in [
                    "Variable"
                ]:
                    replace_strs.append(get_Aggrandizements_name(
                        attachmentsByRange_value, identifier2return_value))
                else:
                    print(json.dumps(attachmentsByRange_value, indent=4))
                    raise ValueError("Unknown data type.")
            # Replace from back to front to prevent positional offset.
            for (start, end), replacement in zip(reversed(matches), reversed(replace_strs)):
                tmp_str = tmp_str[:start] + replacement + tmp_str[end:]
            return tmp_str  # Expressed in string form
        else:
            return str(para_Value)
    elif "Variable" in para_Value and "Type" in para_Value:
        Variable = para_Value["Variable"]
        if "attachmentsByRange" not in Variable:
            Value = Variable["Value"]
            return get_Aggrandizements_name(Value, identifier2return_value)
        else:
            tmp_str = Value["string"]
            matches = [match.start()
                       for match in re.finditer(r'\ufffc', tmp_str)]
            replace_strs = []
            attachmentsByRange_values = list(
                Value["attachmentsByRange"].values())
            for attachmentsByRange_value in attachmentsByRange_values:
                if "OutputUUID" in attachmentsByRange_value and \
                        "Type" in attachmentsByRange_value:
                    OutputUUID = attachmentsByRange_value["OutputUUID"]
                    replace_strs.append(identifier2return_value[OutputUUID])
                elif "OutputUUID" in attachmentsByRange_value and \
                    "Type" in attachmentsByRange_value and \
                        "OutputName" in attachmentsByRange_value:
                    OutputName = attachmentsByRange_value["OutputName"]
                    replace_strs.append(OutputName)
                elif "Type" in attachmentsByRange_value and \
                    "OutputUUID" in attachmentsByRange_value and \
                        "OutputName" in attachmentsByRange_value and \
                        "Aggrandizements" in attachmentsByRange_value:
                    replace_strs.append(get_Aggrandizements_name(
                        attachmentsByRange_value, identifier2return_value))
                else:
                    raise ValueError("Unknown data type.")
            # Replace from back to front to prevent positional offset.
            for (start, end), replacement in zip(reversed(matches), reversed(replace_strs)):
                tmp_str = tmp_str[:start] + replacement + tmp_str[end:]
            return tmp_str  # Expressed in string form
    else:  # Custom entities can be either static or dynamic; no action is taken.
        return str(para_Value)  # Expressed in string form


def get_paraname2paravalue(WFWorkflowActionParameters, identifier2return_value):

    paraname2paravalue = {}
    for para_name, para_Value in WFWorkflowActionParameters.items():
        # For primitive data types, directly input the value. The value of a primitive data type corresponds to either a custom entity or a primitive data type.
        if isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool):
            paraname2paravalue[para_name] = para_Value
        # For dictionary data types, categorize and discuss what values to input.
        elif isinstance(para_Value, dict):
            # If using the output of a previous action, then query `identifier2return_value` to fill in the corresponding name.
            paraname2paravalue[para_name] = process_dict_Value2(
                para_Value, identifier2return_value)
        # For list data types, discuss what values to input based on their categorization.
        elif isinstance(para_Value, list):  # No processing is performed.
            paraname2paravalue[para_name] = str(para_Value)  # Expressed in string form

    return paraname2paravalue


def generate_suitable_ParameterSummary(
    WFWorkflowActionIdentifier,
    WFWorkflowActionParameters,
    identifier2return_value,
    api2paraname2paratype,
    api2parasummary,
    act_paras_that_is_necessary_in_query
):
    
    """Generate the expression seen by each user for each action based on the given parameter names and values:
    - The format for each generated line is:
    - Action description; parameter name=parameter value, parameter name=parameter value, ...; return value name->"return value name"; parameters and values that must appear in the query.

    - Use a greedy matching method to match the `ParameterSummary`. (Exact matching would require considering dependencies, but greedy matching generally ensures correctness.)
    """

    ret_str = f"{WFWorkflowActionIdentifier}; "

    """Match the most suitable `ParameterSummary` from `all_api2parasummary` based on `WFWorkflowActionParameters`:
    - Determine what the selected parameter name in `ParameterSummary` should be:
    - For inputs of primitive data types, use the parameter value.
    - For inputs of enum data types, use the DisplayName of the enum value.
    - For actions using the output of a previous action, prioritize using `CustomOutputName`; if unavailable, use the previous action's default output value.
    - For actions using system input, use the system input's Placeholder.
    """
    
    # For input of the Object data type, use the DisplayName of the Object.

    # First, find the most suitable `ParameterSummary` in `api2parasummary` based on `WFWorkflowActionParameters`.
    WFWorkflowActionParameter_keys = copy.deepcopy(
        list(WFWorkflowActionParameters.keys()))
    if "CustomOutputName" in WFWorkflowActionParameter_keys:
        WFWorkflowActionParameter_keys.remove("CustomOutputName")
    if "WFControlFlowMode" in WFWorkflowActionParameter_keys:
        WFWorkflowActionParameter_keys.remove("WFControlFlowMode")  # Remove those unique to control statements
    if "GroupingIdentifier" in WFWorkflowActionParameter_keys:
        WFWorkflowActionParameter_keys.remove("GroupingIdentifier")
    if "ShowWhenRun" in WFWorkflowActionParameter_keys:
        # For third-party apps, the `ShowWhenRun` and `OpenWhenRun` fields may appear.
        WFWorkflowActionParameter_keys.remove("ShowWhenRun")
    if "OpenWhenRun" in WFWorkflowActionParameter_keys:
        WFWorkflowActionParameter_keys.remove("OpenWhenRun")
    if "AppIntentDescriptor" in WFWorkflowActionParameter_keys:
        # For third-party apps, an `AppIntentDescriptor` field may appear.
        WFWorkflowActionParameter_keys.remove("AppIntentDescriptor")

    ParameterSummary_key, ParameterSummary_value, ParameterSummary_value_list = None, None, None
    if len(api2parasummary) == 1:  # Direct use
        ParameterSummary_key = list(api2parasummary.keys())[0]
        ParameterSummary_value = list(api2parasummary.values())[0]
        reserve_indexs = [ParameterSummary_key]
    else:
        # Find the largest intersection between `WFWorkflowActionParameter_keys` and `cur_api2parasummary_value_list`.
        max_intersection_set_values = [[]]
        reserve_indexs = []
        for key, cur_api2parasummary_value in api2parasummary.items():
            pattern = re.compile(r'\$\{(\w+)\}')
            cur_api2parasummary_value_list = pattern.findall(
                cur_api2parasummary_value)

            cur_intersection_set_value = list(
                set(WFWorkflowActionParameter_keys) & set(cur_api2parasummary_value_list))
            if len(cur_intersection_set_value) > len(max_intersection_set_values[0]):
                max_intersection_set_values = [cur_intersection_set_value]
                reserve_indexs = [key]
            elif len(cur_intersection_set_value) == len(max_intersection_set_values[0]):
                max_intersection_set_values.append(cur_intersection_set_value)
                reserve_indexs.append(key)

        new_api2parasummary = {}
        for key in reserve_indexs:
            new_api2parasummary[key] = api2parasummary[key]

        # Find the largest intersection between `WFWorkflowActionParameter_keys` and `cur_api2parasummary_key_list`.
        max_intersection_set_keys = [[]]
        reserve_key = None
        for cur_api2parasummary_key, cur_api2parasummary_value in new_api2parasummary.items():
            cur_api2parasummary_key_list = cur_api2parasummary_key.split(",")
            cur_intersection_set_key = list(
                set(WFWorkflowActionParameter_keys) & set(cur_api2parasummary_key_list))
            if len(cur_intersection_set_key) > len(max_intersection_set_keys[0]):
                max_intersection_set_keys = [cur_intersection_set_key]
                reserve_key = cur_api2parasummary_key
        if reserve_key == None:
            reserve_key = list(new_api2parasummary.keys())[0]
        ParameterSummary_key = reserve_key
        ParameterSummary_value = new_api2parasummary[reserve_key]

    ParameterSummary_key_list = ParameterSummary_key.split(",")
    pattern = re.compile(r'\$\{(\w+)\}')
    ParameterSummary_value_list = pattern.findall(ParameterSummary_value)

    # Prepare the corresponding parameter values for `ParameterSummary_key` and `ParameterSummary_value` based on `WFWorkflowActionParameters`.
    paraname2paravalue = get_paraname2paravalue(
        WFWorkflowActionParameters, identifier2return_value)

    """Based on WFWorkflowActionParameters, append the corresponding parameter names and values that were generated at the end."""
    # Iterate through `ParameterSummary_key` and `ParameterSummary_value`, and fill in the corresponding parameter values.
    ParameterSummary_key_dict = {}
    ParameterSummary_value_dict = {}
    for i, cur_key in enumerate(ParameterSummary_key_list):
        if cur_key in paraname2paravalue:
            ParameterSummary_key_dict[cur_key] = paraname2paravalue[cur_key]
        else:
            # Check `api2paraname2paratype` to see if there are default values.
            if cur_key in api2paraname2paratype:
                para_desc = "=".join(
                    api2paraname2paratype[cur_key].split("=")[1:])
                if para_desc:
                    defaultValue = eval(para_desc)
                    ParameterSummary_key_dict[cur_key] = defaultValue
                else:
                    ParameterSummary_key_dict[cur_key] = "${" + cur_key + "}"
            else:
                ParameterSummary_key_dict[cur_key] = "${" + cur_key + "}"
    for i, cur_value in enumerate(ParameterSummary_value_list):
        if cur_value in paraname2paravalue:
            cur_para_value = paraname2paravalue[cur_value]
            ParameterSummary_value_dict[cur_value] = cur_para_value
            if isinstance(cur_para_value, str):
                ParameterSummary_value = ParameterSummary_value.replace(
                    "${" + cur_value + "}", "${" + cur_value + "}=" + '"' + cur_para_value + '"')
            else:
                ParameterSummary_value = ParameterSummary_value.replace(
                    "${" + cur_value + "}", "${" + cur_value + "}=" + str(cur_para_value))
        else:
            # Check `api2paraname2paratype` to see if there are any default values.
            if cur_value in api2paraname2paratype:
                para_desc = "=".join(
                    api2paraname2paratype[cur_value].split("=")[1:])
                if para_desc:
                    defaultValue = eval(para_desc)
                    ParameterSummary_value_dict[cur_value] = defaultValue
                    if isinstance(defaultValue, str):
                        ParameterSummary_value = ParameterSummary_value.replace(
                            "${" + cur_value + "}", "${" + cur_value + "}=" + '"' + defaultValue + '"')
                    else:
                        ParameterSummary_value = ParameterSummary_value.replace(
                            "${" + cur_value + "}", "${" + cur_value + "}=" + str(defaultValue))
                else:
                    ParameterSummary_value_dict[cur_value] = r"${" + cur_key + r"}"
            else:
                ParameterSummary_value_dict[cur_value] = r"${" + cur_key + r"}"
    ret_str += ParameterSummary_value

    # Find the difference between `ParameterSummary_key_dict` and `ParameterSummary_value_dict`.
    difference_dict = {}
    for key in ParameterSummary_key_dict:
        if key not in ParameterSummary_value_dict:
            difference_dict[key] = ParameterSummary_key_dict[key]
    ret_str += "; "
    # Obtained in the form of key = value, key = value, ...
    for i, (key, value) in enumerate(difference_dict.items()):
        if not i:
            if isinstance(value, str):
                ret_str += key + "=" + '"' + value + '"'
            else:
                ret_str += key + "=" + str(value)
        else:
            if isinstance(value, str):
                ret_str += ", " + key + "=" + '"' + value + '"'
            else:
                ret_str += ", " + key + "=" + str(value)
    ret_str += "; "

    return_value_name = None
    UUID = None
    if "UUID" in WFWorkflowActionParameters:
        UUID = WFWorkflowActionParameters["UUID"]
        if UUID in identifier2return_value:
            return_value_name = identifier2return_value[UUID]
            ret_str += "ReturnName->${" + return_value_name + "}"
    else:
        if WFWorkflowActionIdentifier in [
            "is.workflow.actions.setvariable",
            "is.workflow.actions.appendvariable",
        ]:
            """"is.workflow.actions.getvariable": Retrieves a variable to pass to the next action. Generates a mapping from the variable name to the original UUID. This UUID must exist (either as the output of a previous action or as a system input).
            Reassigns a variable. Generates a mapping from the variable name to the original UUID. This UUID must exist (either as the output of a previous action or as a system input).
            """
            if "WFVariableName" in WFWorkflowActionParameters:
                return_value_name = WFWorkflowActionParameters["WFVariableName"]
                ret_str += "ReturnName->${" + return_value_name + "}"
    ret_str += "; "

    necessary_keys = []  # Values that appear in the ParameterSummary
    necessary_keys_all = {}
    # Iterate through the `ParameterSummary_value_dict` dictionary to check if its entries are in `para_that_is_necessary_in_query`. 
    # If they are, then those parameters must appear in the query.
    for key, value in ParameterSummary_value_dict.items():
        if key in act_paras_that_is_necessary_in_query:
            necessary_keys.append(key)

    for act_para_key, act_para_val in act_paras_that_is_necessary_in_query.items():  # Not present in the ParameterSummary and not mandatory.
        if act_para_key not in necessary_keys:
            necessary_keys_all[act_para_key] = act_para_val

    tmp_str_list = []
    for j, cur_necessary_key in enumerate(necessary_keys):
        necessary_keys[j] = '${' + cur_necessary_key + '}'
    necessary_key_str = ",".join(necessary_keys)
    if necessary_key_str:
        tmp_str_list.append(necessary_key_str)
    necessary_keys_all_str = ""
    for j, (act_para_key, act_para_val) in enumerate(necessary_keys_all.items()):
        if j == 0:
            if isinstance(act_para_val, str):
                necessary_keys_all_str += '${' + \
                    f'{act_para_key}' + '}="' + act_para_val + '"'
            else:
                necessary_keys_all_str += '${' + \
                    f'{act_para_key}' + '}=' + str(act_para_val)
        else:
            if isinstance(act_para_val, str):
                necessary_keys_all_str += ',${' + \
                    f'{act_para_key}' + '}="' + act_para_val + '"'
            else:
                necessary_keys_all_str += ',${' + \
                    f'{act_para_key}' + '}=' + str(act_para_val)
    if necessary_keys_all_str:
        tmp_str_list.append(necessary_keys_all_str)
    tmp_str = ','.join(tmp_str_list)
    if tmp_str:
        ret_str += "Parameter " + tmp_str + " is necessary in query."
    ret_str += "\n"

    return ret_str


def get_all_shortcuts_paras_that_is_necessary_in_query(final_detailed_records, all_api2paraname2paratype):
    """Retrieve all parameters that must appear in the query for all shortcuts.
    We will only consider parameters that are of primitive (not include string) or enum data types in both the API description and the JSON file as required parameters.
    
    Return:
        Return a three-level nested dictionary: 
        the first level indicates the shortcut, the second level indicates the position of the action in the original shortcut 
        (to identify the API name), 
        and the third level indicates the parameter name 
        (to identify which parameters need to appear in the query).
    """
    all_shortcuts_paras_that_is_necessary_in_query = {}

    for i, cur_shortcut in enumerate(final_detailed_records):
        URL = cur_shortcut["URL"]
        shortcut = cur_shortcut["shortcut"]
        if shortcut is None:
            continue

        WFWorkflowActions = shortcut["WFWorkflowActions"]
        for action_pos, WFWorkflowAction in enumerate(WFWorkflowActions):
            WFWorkflowActionIdentifier = WFWorkflowAction["WFWorkflowActionIdentifier"]

            if WFWorkflowActionIdentifier in [ # These API parameters do not need to be saved.
                "is.workflow.actions.comment",
                "is.workflow.actions.alert",
                "is.workflow.actions.conditional",
                "is.workflow.actions.choosefrommenu",
                "is.workflow.actions.repeat.count",
                "is.workflow.actions.repeat.each",
                "is.workflow.actions.getvariable",
                "is.workflow.actions.setvariable",
                "is.workflow.actions.appendvariable"
            ]:
                continue

            if WFWorkflowActionIdentifier not in all_api2paraname2paratype:
                continue

            WFWorkflowActionParameters = copy.deepcopy(WFWorkflowAction["WFWorkflowActionParameters"])
            WFWorkflowActionParameters.pop("UUID", None) # Identify the output of an action
            WFWorkflowActionParameters.pop("CustomOutputName", None) # An action may have a CustomOutputName field.
            WFWorkflowActionParameters.pop("WFControlFlowMode", None) # Only branches and loops have this.
            WFWorkflowActionParameters.pop("GroupingIdentifier", None)
            WFWorkflowActionParameters.pop("ShowWhenRun", None)
            WFWorkflowActionParameters.pop("OpenWhenRun", None)
            WFWorkflowActionParameters.pop("AppIntentDescriptor", None) # For third-party apps, an AppIntentDescriptor field may appear.
            
            """We will only consider parameters that are of primitive (not include string) or enum data types in both the API description and the JSON file as required parameters.
            """
            for para_name, para_Value in WFWorkflowActionParameters.items():
                if isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool):
                    
                    # print(WFWorkflowActionIdentifier, para_name)
                    if WFWorkflowActionIdentifier not in all_api2paraname2paratype or para_name not in all_api2paraname2paratype[
                        WFWorkflowActionIdentifier]:
                        continue
                    
                    para_type_and_default_value = all_api2paraname2paratype[WFWorkflowActionIdentifier][para_name]
                    para_type = para_type_and_default_value.split("=")[0].strip()
                    para_default_value = None
                    if len(para_type_and_default_value.split("=")) > 1:
                        para_default_value = para_type_and_default_value.split("=")[1].strip()

                    # It was found that many strings are too long, and therefore will not be considered as required parameters.
                    if isinstance(para_Value, str) and len(para_Value) > 300:
                        continue
                    
                    """String type parameters are difficult to categorize as strictly necessary, semantically precise, or unnecessary. 
                    Therefore, string type evaluations will be temporarily excluded.
                    """
                    # if isinstance(para_Value, str) and para_type == "String" or \
                    #     isinstance(para_Value, int) and para_type == "Integer" or \
                    #         isinstance(para_Value, float) and para_type == "Float" or \
                    # isinstance(para_Value, bool) and para_type == "Bool" or \
                    # isinstance(para_Value, str) and para_type == "Enum":

                    if isinstance(para_Value, int) and para_type == "Integer" or \
                        isinstance(para_Value, float) and para_type == "Float" or \
                        isinstance(para_Value, bool) and para_type == "Bool" or \
                        isinstance(para_Value, str) and para_type == "Enum":
                        if URL not in all_shortcuts_paras_that_is_necessary_in_query:
                            all_shortcuts_paras_that_is_necessary_in_query[URL] = {}
                        if action_pos not in all_shortcuts_paras_that_is_necessary_in_query[URL]:
                            all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos] = {}
                        all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos][para_name] = para_Value
                    # String type parameters are difficult to categorize as strictly necessary, semantically precise, or unnecessary. 
                    # Therefore, string type evaluations will be temporarily excluded.
                    # # Integer, float, string, and boolean types can be converted to each other.
                    # elif para_type == "String" and (isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool)):
                    #     if URL not in all_shortcuts_paras_that_is_necessary_in_query:
                    #         all_shortcuts_paras_that_is_necessary_in_query[URL] = {
                    #         }
                    #     if action_pos not in all_shortcuts_paras_that_is_necessary_in_query[URL]:
                    #         all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos] = {
                    #         }
                    #     all_shortcuts_paras_that_is_necessary_in_query[
                    #         URL][action_pos][para_name] = para_Value
                    elif para_type == "Integer" and (isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool)):
                        if isinstance(para_Value, str) and para_Value.isnumeric() or \
                                isinstance(para_Value, int) or \
                            isinstance(para_Value, float) or \
                                isinstance(para_Value, bool):
                            if URL not in all_shortcuts_paras_that_is_necessary_in_query:
                                all_shortcuts_paras_that_is_necessary_in_query[URL] = {
                                }
                            if action_pos not in all_shortcuts_paras_that_is_necessary_in_query[URL]:
                                all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos] = {
                                }
                            all_shortcuts_paras_that_is_necessary_in_query[
                                URL][action_pos][para_name] = para_Value
                    elif para_type == "Float" and (isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool)):
                        if isinstance(para_Value, str) and para_Value.replace(".", "", 1).isnumeric() or \
                                isinstance(para_Value, int) or \
                            isinstance(para_Value, float) or \
                                isinstance(para_Value, bool):
                            if URL not in all_shortcuts_paras_that_is_necessary_in_query:
                                all_shortcuts_paras_that_is_necessary_in_query[URL] = {
                                }
                            if action_pos not in all_shortcuts_paras_that_is_necessary_in_query[URL]:
                                all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos] = {
                                }
                            all_shortcuts_paras_that_is_necessary_in_query[
                                URL][action_pos][para_name] = para_Value
                    elif para_type == "Bool" and (isinstance(para_Value, str) or isinstance(para_Value, int) or isinstance(para_Value, float) or isinstance(para_Value, bool)):
                        if isinstance(para_Value, str) and para_Value.lower() in ["true", "false"] or \
                                isinstance(para_Value, int) and para_Value in [0, 1] or \
                            isinstance(para_Value, float) and para_Value in [0.0, 1.0] or \
                                isinstance(para_Value, bool):
                            if URL not in all_shortcuts_paras_that_is_necessary_in_query:
                                all_shortcuts_paras_that_is_necessary_in_query[URL] = {
                                }
                            if action_pos not in all_shortcuts_paras_that_is_necessary_in_query[URL]:
                                all_shortcuts_paras_that_is_necessary_in_query[URL][action_pos] = {
                                }
                            all_shortcuts_paras_that_is_necessary_in_query[
                                URL][action_pos][para_name] = para_Value
                            
    return all_shortcuts_paras_that_is_necessary_in_query


def get_identifier2return_value(WFWorkflowActions, all_api2paraname2paratype):
    """Generate a mapping from UUID to the action's return value name. If there is no return value name, this field is absent.
    - If there is a CustomOutputName, prioritize using CustomOutputName for the UUID mapping. The default return value name should also be included afterwards. The default return value name is identified in `all_api2paraname2paratype` with a key starting with "ThisIsReturnValue:".
    Having the UUID to return value name mapping allows us to determine which previous output the current action uses, clarifying what needs to be filled in the `ParameterSummary`.

    For assignment statements, generate variable names, with the return value name being the variable name of the assignment statement.
    - `is.workflow.actions.getvariable`: Retrieves a variable to pass to the next action. Generate a mapping from the variable name to the original UUID. This UUID must exist (either as a previous action's output or as a system input).
    - `is.workflow.actions.setvariable`: Reassigns a variable. Generate a mapping from the variable name to the original UUID. This UUID must exist (either as a previous action's output or as a system input).
    - `is.workflow.actions.appendvariable`: Appends a value to a variable. Generate a mapping from the variable name to the original UUID. This UUID must exist (either as a previous action's output or as a system input).
    """

    identifier2return_value = {}
    for WFWorkflowAction in WFWorkflowActions:
        WFWorkflowActionIdentifier = WFWorkflowAction["WFWorkflowActionIdentifier"]
        if WFWorkflowActionIdentifier not in all_api2paraname2paratype:
            continue

        WFWorkflowActionParameters = copy.deepcopy(WFWorkflowAction["WFWorkflowActionParameters"])
        WFWorkflowActionParameters.pop("ShowWhenRun", None) # For third-party apps, the fields `ShowWhenRun` and `OpenWhenRun` may appear.
        WFWorkflowActionParameters.pop("OpenWhenRun", None)
        WFWorkflowActionParameters.pop("AppIntentDescriptor", None) # For third-party apps, an `AppIntentDescriptor` field may appear.

        UUID = None
        if "UUID" in WFWorkflowActionParameters:
            UUID = WFWorkflowActionParameters["UUID"]
            CustomOutputName = None
            if "CustomOutputName" in WFWorkflowActionParameters:
                CustomOutputName = WFWorkflowActionParameters["CustomOutputName"]
            DefaultOutputName = None
            # If the dictionary `all_api2paraname2paratype[WFWorkflowActionIdentifier]` contains a key starting with "ThisIsReturnValue:", 
            # then this key is the default return value name. Retrieve the value associated with this key.
            if WFWorkflowActionIdentifier in all_api2paraname2paratype:
                para_keys = list(all_api2paraname2paratype[WFWorkflowActionIdentifier].keys())
                for para_key in para_keys:
                    if para_key.startswith("ThisIsReturnValue:"):
                        DefaultOutputName = para_key[len("ThisIsReturnValue:"):].strip()
                        break
            if CustomOutputName and not DefaultOutputName:
                identifier2return_value[UUID] = CustomOutputName
            elif not CustomOutputName and DefaultOutputName:
                identifier2return_value[UUID] = DefaultOutputName
            elif CustomOutputName and DefaultOutputName:
                identifier2return_value[UUID] = CustomOutputName
            else:
                specialapi2name = {}
                # raise ValueError("CustomOutputName and DefaultOutputName cannot both be empty.") # Some actions have a UUID but no actual return value......
                pass
        else:
            """
            "is.workflow.actions.conditional"
            "is.workflow.actions.choosefrommenu",
            "is.workflow.actions.repeat.each"
            "is.workflow.actions.repeat.count"
            "is.workflow.actions.getvariable"
            "is.workflow.actions.setvariable"
            "is.workflow.actions.appendvariable"

            The output of the previous action's variable includes a variable name:
                "WFWorkflowActionParameters": {
                    "WFInput": {
                        "Value": {
                            "OutputUUID": "6C7405A7-5E3F-4AA9-83EB-D0191894D44B",
                            "Type": "ActionOutput",
                            "OutputName": "Elemento scelto"
                        },
                        "WFSerializationType": "WFTextTokenAttachment"
                    },
                    "WFVariableName": "selected"
                }
            When the current action wants to reference a previous action:
                "WFWorkflowActionParameters": {
                    "WFInput": {
                        "Value": {
                            "VariableName": "selected", # Only the variable name is mentioned here.
                            "Type": "Variable"
                        },
                        "WFSerializationType": "WFTextTokenAttachment"
                    },
                    "UUID": "D06FFAF7-3D6D-4E89-B4D2-8EE62432D539"
                }

            # "is.workflow.actions.comment"
            # "is.workflow.actions.getitemfromlist" # No special handling required.
            # "is.workflow.actions.choosefromlist"
            # "is.workflow.actions.getitemtype"
            # "is.workflow.actions.getitemname"
            """
            if WFWorkflowActionIdentifier in [
                "is.workflow.actions.setvariable",
                "is.workflow.actions.appendvariable",
            ]:
                # "is.workflow.actions.getvariable": Retrieves a variable to pass to the next action. Generates a mapping from the variable name to the original UUID. This UUID must exist (either as the output of a previous action or as a system input).
                # Reassigns a variable. Generates a mapping from the variable name to the original UUID. This UUID must exist (either as the output of a previous action or as a system input).
                
                if "WFVariableName" in WFWorkflowActionParameters:
                    WFVariableName = WFWorkflowActionParameters["WFVariableName"]
                    if "WFInput" in WFWorkflowActionParameters:
                        WFInput = WFWorkflowActionParameters["WFInput"]
                        if isinstance(WFInput, dict):
                            if len(WFInput) == 2 and "Value" in WFInput and "WFSerializationType" in WFInput:
                                Value = WFInput["Value"]
                                if "OutputUUID" in Value:
                                    OutputUUID = Value["OutputUUID"]
                                    Type = Value["Type"]
                                    OutputName = None
                                    if "OutputName" in Value:
                                        OutputName = Value["OutputName"]                                    
                                    identifier2return_value[WFVariableName] = OutputUUID # The return value name can be found using the UUID.
                                else:
                                    identifier2return_value[WFVariableName] = WFVariableName
                        else:
                            raise ValueError("WFInput is not a dictionary.")
                    else:
                        identifier2return_value[WFVariableName] = WFVariableName
            else:
                continue

    return identifier2return_value


if __name__ == "__main__":

    SHORTCUT_DATA = os.getenv("SHORTCUT_DATA")
    
    final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)

    WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "WorkflowKit.framework/Versions/A/Resources/WFActions.json")
    wf_actions_instance = WFActionsClass(WFActions_path)
    """We found that some description files in WFActions.json were lacking relevant information. 
    As a result, we manually supplemented them based on parameter examples from JSON format shortcuts.
    """
    my_WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "my_WFActions.json")
    wf_actions_instance.WFActions_dicts.update(json.load(open(my_WFActions_path, "r")))
    all_api2info_WF, all_api2paraname2paratype_WF, all_api2parasummary_WF = wf_actions_instance.all_api2desc(
        need_api2paraname2paratype=True, need_api2parasummary=True)

    """Load definition files from the App"""
    # succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_success_api_json_filter.json")
    # fail_api_json_path = os.path.join(SHORTCUT_DATA, "4_fail_api_json_filter.json")
    # API_instance = APIsClass(succ_api_json_path, fail_api_json_path)
    api_json_path = os.path.join(SHORTCUT_DATA, "4_api_json_filter.json")
    API_instance = APIsClass(api_json_path)
    all_api2info_from_app, all_api2paraname2paratype_from_app, all_api2parasummary_from_app = API_instance.all_api2desc(
        need_api2paraname2paratype=True, need_api2parasummary=True)

    """Mapping of all API to API information"""
    all_api2info = all_api2info_WF.copy()
    all_api2info.update(all_api2info_from_app)
    print(len(all_api2info_WF), len(all_api2info_from_app),len(all_api2info)) # 1414
    # with open(os.path.join(SHORTCUT_DATA, tmp, "all_api2info.json"), "w") as f:
    #     json.dump(all_api2info, f, indent=4, ensure_ascii=False)

    """Mapping of all APIs to parameter names and parameter types (including default values)"""
    all_api2paraname2paratype = all_api2paraname2paratype_WF.copy()
    all_api2paraname2paratype.update(all_api2paraname2paratype_from_app)
    # with open(os.path.join(SHORTCUT_DATA, "tmp", "all_api2paraname2paratype.json"), "w") as f:
    #     json.dump(all_api2paraname2paratype, f, indent=4, ensure_ascii=False)

    """Mapping of all APIs to User-friendly API descriptions"""
    all_api2parasummary = all_api2parasummary_WF.copy()
    all_api2parasummary.update(all_api2parasummary_from_app)
    # Apply special handling to the following: remove duplicates based on values. If they are too long, randomly retain one key.
    special_keys = [
        "com.joehribar.toggl.CheckTimeLoggedIntent",
        "com.joehribar.toggl.UpdateTimeEntryIntent",
        "com.joehribar.toggl.GetTimeEntriesIntent",
        "com.joehribar.toggl.GetSavedTimersIntent",
        "com.joehribar.toggl.GetRecentTimeEntriesIntent"
    ]
    for special_key in special_keys:
        if special_key in all_api2parasummary:
            special_dict = all_api2parasummary[special_key]
            special_dict = dict( # Remove duplicates based on values, retaining the deduplicated values and their corresponding keys.
                zip(special_dict.values(), special_dict.keys()))
            all_api2parasummary[special_key] = special_dict
    # with open(os.path.join(SHORTCUT_DATA, "tmp", "all_api2parasummary.json"), "w") as f:
    #     json.dump(all_api2parasummary, f, indent=4, ensure_ascii=False)

    all_shortcuts_paras_that_is_necessary_in_query = get_all_shortcuts_paras_that_is_necessary_in_query(
        final_detailed_records, all_api2paraname2paratype)

    # with open(os.path.join(SHORTCUT_DATA, "tmp", "all_shortcuts_paras_that_is_necessary_in_query.json"), "w") as f:
    #     json.dump(all_shortcuts_paras_that_is_necessary_in_query, f, indent=4, ensure_ascii=False)

    shortcut2desc = {}
    for i, cur_shortcut in enumerate(final_detailed_records):
        URL = cur_shortcut["URL"]
        shortcut = cur_shortcut["shortcut"]
        if shortcut is None:
            continue

        WFWorkflowActions = shortcut["WFWorkflowActions"]
        identifier2return_value = get_identifier2return_value(
            WFWorkflowActions, all_api2paraname2paratype)

        if URL in all_shortcuts_paras_that_is_necessary_in_query:
            shortcut_paras_that_is_necessary_in_query = all_shortcuts_paras_that_is_necessary_in_query[URL]
        else:
            shortcut_paras_that_is_necessary_in_query = {}

        desc_str = generate_shortcutdesc(
            WFWorkflowActions,
            identifier2return_value,
            all_api2paraname2paratype,
            all_api2parasummary,
            shortcut_paras_that_is_necessary_in_query,
            depth=0
        )
        shortcut2desc[URL] = desc_str

    # SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
    # with open(os.path.join(SHORTCUT_DATA, "tmp", "shortcut2desc.json"), "w") as wp:
    #     json.dump(shortcut2desc, wp, indent=4, ensure_ascii=False)
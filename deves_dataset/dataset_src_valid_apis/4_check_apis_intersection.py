"""Perform an intersection check between the shortcuts and the collected API set.
"""

import json
import os

from APIs_to_be_filtered_out import no_apps_or_apis, mobile_only_apis, paid_apps, discoverable_false_apis
no_apps_or_apis.extend(mobile_only_apis)
no_apps_or_apis.extend(paid_apps)
no_apps_or_apis.extend(discoverable_false_apis)

SHORTCUT_PROJECT = os.getenv("SHORTCUT_PROJECT", "")
if SHORTCUT_PROJECT == "":
    raise Exception("The SHORTCUT_PROJECT environment variable is not set.")
SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The SHORTCUT_DATA environment variable is not set.")

# All APIs in shortcuts
# final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis.json")
# final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_remove_repeat.json")
with open(final_detailed_records_path, "r") as f:
    final_detailed_records = json.load(f)
print(f"Number of retrieved shortcuts: {len(final_detailed_records)}")
# exit(0)

# Manually filter out certain APIs
new_detailed_records = []
for cur_record in final_detailed_records:
    if "shortcut" not in cur_record:
        pass
    elif cur_record["shortcut"] is None:
        pass
    else:
        WFWorkflowActions = cur_record["shortcut"]["WFWorkflowActions"]
        break_second = False
        remove_or_not = False
        for WFWorkflowAction in WFWorkflowActions:
            for name_contain in no_apps_or_apis:
                if name_contain in WFWorkflowAction["WFWorkflowActionIdentifier"]:
                    remove_or_not = True
                    break_second = True
                    break
            if break_second:
                break
        if remove_or_not:
            continue
        new_detailed_records.append(cur_record)
final_detailed_records = new_detailed_records
len_after_remove_manual = len(final_detailed_records)
print(f"After removing non-existent APIs: {len_after_remove_manual}")
print()
# exit(0)

api_names_in_shortcuts = []
for cur_record in final_detailed_records:
    if "shortcut" not in cur_record:
        pass
    elif cur_record["shortcut"] is None:
        pass
    else:
        WFWorkflowActions = cur_record["shortcut"]["WFWorkflowActions"]
        break_second = False
        for WFWorkflowAction in WFWorkflowActions:
            api_names_in_shortcuts.append(WFWorkflowAction["WFWorkflowActionIdentifier"])
# All APIs retrieved from shortcuts
api_names_in_shortcuts = list(set(api_names_in_shortcuts))
print(f"Number of APIs in shortcuts: {len(api_names_in_shortcuts)}")

succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_success_api_json_filter.json")
with open(succ_api_json_path, "r") as f:
    succ_api_json = json.load(f)
fail_list_json_actionsdata_path = os.path.join(SHORTCUT_DATA, "4_fail_api_json_filter.json")
with open(fail_list_json_actionsdata_path, "r") as f:
    fail_api_json = json.load(f)
succ_api_json.extend(fail_api_json)

# Extract all actionsData and intentDefinition from success_list_json_actionsdata to form a set of api_names.
valid_names_actionsdata = []
all_names_actionsdata = []
valid_names_intentdefinition = []
for cur_json in succ_api_json:
    AppName = cur_json["AppName"]
    keys = list(cur_json.keys())
    for cur_key in keys:
        if "actionsdata" in cur_key:
            actionsdata = cur_json[cur_key]
            for action_name, action_val in actionsdata["actions"].items():
                if "isDiscoverable" not in action_val:
                    valid_names_actionsdata.append(".".join([AppName, action_name]))
                elif action_val["isDiscoverable"] == True:
                    valid_names_actionsdata.append(".".join([AppName, action_name]))
                all_names_actionsdata.append(".".join([AppName, action_name]))
        if "intentdefinition" in cur_key:
            intentdefinition = cur_json[cur_key]
            INIntents = intentdefinition["INIntents"]
            for INIntent in INIntents:
                INIntentName = INIntent["INIntentName"]

                prefix_intentname = ""
                if "INIntentClassPrefix" in INIntent:
                    prefix_intentname = INIntent["INIntentClassPrefix"]
                INIntentName = prefix_intentname + INIntentName

                if "Intent" not in INIntentName:
                    INIntentName = INIntentName + "Intent"
                valid_names_intentdefinition.append(".".join([AppName, INIntentName]))

valid_names_actionsdata = list(set(valid_names_actionsdata))
valid_names_intentdefinition = list(set(valid_names_intentdefinition))

# Combine with is.workflow.actions and WorkflowKit.framework/Resources/WFActions.json.
WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "WorkflowKit.framework/Versions/A/Resources/WFActions.json")
WFActions = []
with open(WFActions_path, "r") as f:
    WFActions = json.load(f)
valid_names_actionsdata.extend(WFActions)

# Check the intersection of valid_names_xx and api_names_in_shortcuts.
intersection_actionsdata = list(set(valid_names_actionsdata) & set(api_names_in_shortcuts))
intersection_intentdefinition = list(set(valid_names_intentdefinition) & set(api_names_in_shortcuts))

print(f"Number of APIs in valid_names_actionsdata: {len(valid_names_actionsdata)}")
print(f"Number of APIs in valid_names_intentdefinition: {len(valid_names_intentdefinition)}")
print()

print(f"Number of APIs in intersection_actionsdata: {len(intersection_actionsdata)}")
print(f"Number of APIs in intersection_intentdefinition: {len(intersection_intentdefinition)}")

# Print APIs present in shortcuts but not in valid_names_xx, sorted in lexicographical order
print("APIs present in shortcuts but not in valid_names_xx:")

api_names_in_shortcuts_not_in_valid_names = list(set(api_names_in_shortcuts) - set(valid_names_actionsdata + valid_names_intentdefinition))
print(sorted(api_names_in_shortcuts_not_in_valid_names))
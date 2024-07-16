"""筛掉那些在filter_apis.py中指定的需要筛除的APIs。
"""

import os
import json
from APIs_to_be_filtered_out import no_apps_or_apis, mobile_only_apis, paid_apps, discoverable_false_apis
no_apps_or_apis.extend(mobile_only_apis)
no_apps_or_apis.extend(paid_apps)
no_apps_or_apis.extend(discoverable_false_apis)

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA")

final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_remove_repeat.json")
dump_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis.json")

# final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis.json")
# dump_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis.json")

# final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
# dump_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")

with open(final_detailed_records_path, "r") as rp:
    final_detailed_records = json.load(rp)

unique_id2file_name = {}
file_names = set()
for i, cur_shortcut in enumerate(final_detailed_records):
    URL = cur_shortcut["URL"]
    if URL is None:
        continue
    # https://www.icloud.com/shortcuts/e6fa8dd9e012484bb85c9967f0b83f02
    unique_id = URL.split("/")[-1]
    
    if "records" not in cur_shortcut or cur_shortcut["records"] is None:
        continue
    file_name = cur_shortcut["records"]["fields"]["name"]["value"]
    file_name = file_name.replace("/", " OR ")
    if len(file_name) >= 1 and file_name[0] == ".":
        file_name = file_name[1:]
    if len(file_name) < 1:
        continue

    unique_id2file_name[unique_id] = file_name
    file_names.add(file_name)
    
# 记录每一个快捷指令的长度
filter_because_of_lacking_related_shortcuts = 0
continue_num = 0
no_WFWorkflowName_num = 0
new_final_detailed_records = []
for i, cur_shortcut in enumerate(final_detailed_records):
    URL = cur_shortcut["URL"]
    if (i + 1) % 100 == 0:
        print(f"正在处理第 {i + 1} 个文件, URL为 {URL}.")

    shortcut = cur_shortcut["shortcut"]
    if shortcut is None:
        continue
    
    WFWorkflowActions = shortcut["WFWorkflowActions"]

    break_second = False
    remove_or_not = False
    for WFWorkflowAction in WFWorkflowActions:
        # if WFWorkflowAction["WFWorkflowActionIdentifier"] == "is.workflow.actions.runworkflow":
        #     if "WFWorkflowActionParameters" not in  WFWorkflowAction or "WFWorkflowName" not in WFWorkflowAction["WFWorkflowActionParameters"]:
        #         no_WFWorkflowName_num += 1
        #         remove_or_not = True
        #         break
        #     else:
        #         WFWorkflowName = WFWorkflowAction["WFWorkflowActionParameters"]["WFWorkflowName"]
        #         # print(json.dumps(WFWorkflowName, indent=4, ensure_ascii=False))

        #         if isinstance(WFWorkflowName, str):
        #             WFWorkflowName = WFWorkflowName.replace("/", " OR ")
        #             if len(WFWorkflowName) >= 1 and WFWorkflowName[0] == ".":
        #                 WFWorkflowName = WFWorkflowName[1:]
        #             if len(WFWorkflowName) < 1:
        #                 raise Exception("file_name长度小于1")

        #             if WFWorkflowName not in file_names:
        #                 remove_or_not = True
        #                 filter_because_of_lacking_related_shortcuts += 1
        #                 break
        #         else:
        #             continue_num += 1
        
        for name_contain in no_apps_or_apis:
            if name_contain in WFWorkflowAction["WFWorkflowActionIdentifier"]:
                remove_or_not = True
                break_second = True
                break
        if break_second:
            break
    if remove_or_not:
        continue
    new_final_detailed_records.append(cur_shortcut)

print("filter_because_of_lacking_related_shortcuts:", filter_because_of_lacking_related_shortcuts)
print("no_WFWorkflowName_num:", no_WFWorkflowName_num)
print(f"筛选后剩余的快捷指令数量：{len(new_final_detailed_records)}")

# 保存筛选后的结果
ignore_in_judge_WFWorkflowActionIdentifier_list = [  # 不计算在评测结果中的动作
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
filter_WFWorkflowActionIdentifier_list = [  # 直接剔除，既不计算在评测结果，也不作为智能体的输入的快捷指令（智能体看不到这个comment）
    "is.workflow.actions.comment",
    "is.workflow.actions.alert"
]

avg_APIs = []
avg_Actions = []
API_set = set()
for i, cur_shortcut in enumerate(new_final_detailed_records):
    shortcut = cur_shortcut["shortcut"]
    if shortcut is None:
        continue
    WFWorkflowActions = shortcut["WFWorkflowActions"]
    APIs, Actions = [], []
    for WFWorkflowAction in WFWorkflowActions:
        if WFWorkflowAction["WFWorkflowActionIdentifier"] in ignore_in_judge_WFWorkflowActionIdentifier_list:
            continue
        if WFWorkflowAction["WFWorkflowActionIdentifier"] in filter_WFWorkflowActionIdentifier_list:
            continue
        APIs.append(WFWorkflowAction["WFWorkflowActionIdentifier"])
        Actions.append(WFWorkflowAction["WFWorkflowActionIdentifier"])
        API_set.add(WFWorkflowAction["WFWorkflowActionIdentifier"])
    APIs = list(set(APIs)) # 7.68
    avg_APIs.append(len(APIs))
    avg_Actions.append(len(Actions))

print(f"筛选后的结果中，每个快捷指令涉及的APIs的平均个数为：{sum(avg_APIs) / len(avg_APIs)}")
print(f"筛选后的结果中，每个快捷指令涉及的Actions的平均个数为：{sum(avg_Actions) / len(avg_Actions)}") # 21.46
print(f"筛选后的结果中，涉及的APIs的个数为：{len(API_set)}")

# 保存筛选后的结果
with open(dump_detailed_records_path, "w") as wp:
    json.dump(new_final_detailed_records, wp, indent=4, ensure_ascii=False)
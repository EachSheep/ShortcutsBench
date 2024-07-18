"""Generate function descriptions and queries for shortcuts.

Specific requirements include:
1. Include values for all primitive data types and enumerated data types in the queries.
2. Exclude values for all system parameters from the queries.
"""

import json
import os
import time
import sys
from generate_shortcut_desc import WFActionsClass, APIsClass
import openai
import tiktoken

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The environment variable SHORTCUT_DATA is not configured.")
sys.path.append(SHORTCUT_DATA)

from cal_shortcut_len import cal_WFWorkflowActions_len

"""When using GPT-4 series models, please be mindful of your expenses. Generating queries cost us hundreds of dollars.
"""
client = openai.OpenAI()
model_name = "gpt-4o"
input_price_every_million, output_price_every_million = 5, 15
input_token_count = 0
output_token_count = 0

SYSTEM_PROMPT_TEMPLATE = """
Shortcut consist of a sequence of actions, each is an API call, to execute user-provided queries. 

As a user-friendly and patient inquirer, you need to craft a query based on the provided shortcut. This query, formatted as a question, should describe the task a user wants to complete and adhere to the following criteria:
1. The problem described in the query must be solvable using the shortcut.
2. The query should include all required parameters from the shortcut.
3. The query should be naturally phrased, integrating parameters seamlessly into the question rather than listing them separately.

For each shortcut command, I will provide you with five fields:
1. 'RecordName': The name of the shortcut, briefly describing its function.
2. 'Description of the Shortcut Workflow': A description of the entire action workflow of the shortcut.
3. 'Comments': Optional. Notes from the shortcut's developer, which may describe its functions or other features.
4. 'Description in Store': A description of the shortcut’s functionality provided in the shortcut store.
5. 'API Description List': Detailed descriptions of the APIs involved in the shortcut.

You should rely primarily on the 'Description of the Shortcut Workflow' and 'API Description List', and refer to 'RecordName', 'Comments', and 'Description in Store' to formulate the final query.

The 'Description of the Shortcut Workflow' details the entire action workflow of the shortcut, with each line representing an API call. Each line is divided into five parts by semicolons:
1. The API's name.
2. A natural language description of the function performed by the API call, including parameter values presented as ${ParaName}=ParaValue.
3. Any additional parameters and their values required by the API call, which may not be mentioned in part 2.
4. The name of the API call's return value, which may be empty.
5. Specific parameter values that you must integrate into the query you generate, which may also be empty.

Parameter values might be basic data types like strings, integers, floats, or booleans, directly represented by the parameter values, or they could be outputs from previous API calls (indicated by parameter names), files provided by the user (${Ask for ExtensionInput}), user inputs (${Ask User}), the current date (${Ask for CurrentDate}), clipboard contents (${Ask for Clipboard}), details about the user’s device (${Ask for DeviceDetails}), or other parameters which might be dictionaries or lists.

The 'Description of the Shortcut Workflow' may also include conditional structures ('is.workflow.actions.conditional'), switch structures ('is.workflow.actions.choosefrommenu'), and loop structures ('is.workflow.actions.repeat.count' or 'is.workflow.actions.repeat.each'). If these structures include essential parameters, these should also be detailed in the query.

The 'API Description List' provides a comprehensive description of all APIs that can be invoked by the shortcut. This includes API name, parameter names, parameter types, parameter default values, parameter return value names, and return value types. Additionally, marked with Parameters for parameter names and explanations, Description for a brief and detailed API functionality description, and ParameterSummary for a natural language description of the API.
"""

USER_PROMPT_TEMPLATE = """Below are the five fields I provide to you:
1. 'RecordName': {RecordName}
2. 'Description of the Shortcut Workflow': {DescriptionoftheShortcutWorkflow}
3. 'Comments': {Comments}
4. 'Description in Store': {DescriptionInStore}
5. 'API Description List': {APIDescriptionList}

Please generate a query based on these details. Alongside the query, provide the shortcut's name and a description of its functionality using the following JSON format:
{{
	"shortcut_name": "ThisIsShortcutName",
	"shortcut_description": "ThisIsShortcutDescription",
	"query": "ThisIsQuery"
}}

Do not output any other content; your response should only be in this JSON format. 
Do not simply repeat the shortcut workflow. Parameters not surrounded by `${{}}` should not appear in the generated query.
Output the JSON directly without using ```json XX``` to enclose it.

Note again, you should include all required parameters in the generated query. Please give your answer in English.

Begin!
"""

if __name__ == "__main__":
    
    """Definition file from the Shortcuts app"""
    WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "WorkflowKit.framework/Versions/A/Resources/WFActions.json")
    wf_actions_instance = WFActionsClass(WFActions_path)
    my_WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "my_WFActions.json")
    wf_actions_instance.WFActions_dicts.update(json.load(open(my_WFActions_path, "r")))
    all_api2info_WF, all_api2paraname2paratype_WF, all_api2parasummary_WF = wf_actions_instance.all_api2desc(need_api2paraname2paratype=True, need_api2parasummary=True)

    """Load the definition file from the app."""
    # succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_success_api_json_filter.json")
    # fail_api_json_path = os.path.join(SHORTCUT_DATA, "4_fail_api_json_filter.json")
    # API_instance = APIsClass(succ_api_json_path, fail_api_json_path)
    api_json_path = os.path.join(SHORTCUT_DATA, "4_api_json_filter.json")
    API_instance = APIsClass(api_json_path)
    all_api2info_from_app, all_api2paraname2paratype_from_app, all_api2parasummary_from_app = API_instance.all_api2desc(need_api2paraname2paratype=True, need_api2parasummary=True)

    """APIs to API info"""
    all_api2info = all_api2info_WF.copy()
    all_api2info.update(all_api2info_from_app)
    print(len(all_api2info_WF), len(all_api2info_from_app), len(all_api2info))

    """Mapping of all APIs to parameter names to parameter types (including default values)."""
    all_api2paraname2paratype = all_api2paraname2paratype_WF.copy()
    all_api2paraname2paratype.update(all_api2paraname2paratype_from_app)
    
    # all_api2parasummary = all_api2parasummary_WF.copy()
    # all_api2parasummary.update(all_api2parasummary_from_app)
    # special_keys = [
    #     "com.joehribar.toggl.CheckTimeLoggedIntent", 
    #     "com.joehribar.toggl.UpdateTimeEntryIntent", 
    #     "com.joehribar.toggl.GetTimeEntriesIntent", 
    #     "com.joehribar.toggl.GetSavedTimersIntent",
    #     "com.joehribar.toggl.GetRecentTimeEntriesIntent"
    # ]
    # for special_key in special_keys:
    #     if special_key in all_api2parasummary:
    #         special_dict = all_api2parasummary[special_key]
    #         special_dict = dict(zip(special_dict.values(), special_dict.keys()))
    #         all_api2parasummary[special_key] = special_dict

    final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)

    # Sort `final_detailed_records` in descending order according to the result of the `cal_WFWorkflowActions_len` function.
    final_detailed_records.sort(key=lambda x: cal_WFWorkflowActions_len(x["shortcut"]["WFWorkflowActions"], URL=x["URL"]), reverse=True)

    """Mapping of URLs to shortcuts descriptions."""
    with open(os.path.join(SHORTCUT_DATA, "tmp", "shortcut2desc.json"), "r") as fp:
        shortcut2desc = json.load(fp)
    
    generated_success_path = os.path.join(SHORTCUT_DATA, "tmp", f"generated_success_queries.json")
    if os.path.exists(generated_success_path):
        with open(generated_success_path, "r") as f:
            generated_success_queries = json.load(f)
    else:
        generated_success_queries = {}

    generated_fail_path = os.path.join(SHORTCUT_DATA, "tmp", f"generated_fail_queries.json")
    if os.path.exists(generated_fail_path):
        with open(generated_fail_path, "r") as f:
            generated_fail_queries = json.load(f)
    else:
        generated_fail_queries = {}

    cnt = 0

    for i, cur_shortcut in enumerate(final_detailed_records):
        URL = cur_shortcut["URL"]
        print(f"Generating query for the {i + 1}th shortcut... {URL}, {len(final_detailed_records) - len(generated_success_queries)} shortcuts remaining.")

        if URL in generated_success_queries:
            continue

        shortcut = cur_shortcut["shortcut"]
        if shortcut is None:
            continue
        
        NameINStore = cur_shortcut["NameINStore"][0]
        RecordName = cur_shortcut["records"]["fields"]["name"]["value"]
        DescriptionInStore = cur_shortcut["DescriptionInStore"][0]
        DescriptionoftheShortcutWorkflow = shortcut2desc[URL]
        Comments = None
        APINameList, APIDescriptionList = [], []

        WFWorkflowActions = shortcut["WFWorkflowActions"]
        for WFWorkflowAction in WFWorkflowActions[:1]: # Include only the content of the first Comment.
            WFWorkflowActionIdentifier = WFWorkflowAction["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters = WFWorkflowAction["WFWorkflowActionParameters"]
            if WFWorkflowActionIdentifier in [
                "s.workflow.actions.comment",
                "is.workflow.actions.alert"
                ]:
                if "WFCommentActionText" in WFWorkflowActionParameters:
                    WFCommentActionText = WFWorkflowActionParameters["WFCommentActionText"]
                    Comments = WFCommentActionText
                break
        
        for WFWorkflowAction in WFWorkflowActions:
            WFWorkflowActionIdentifier = WFWorkflowAction["WFWorkflowActionIdentifier"]
            WFWorkflowActionParameters = WFWorkflowAction["WFWorkflowActionParameters"]
            if WFWorkflowActionIdentifier in [
                "is.workflow.actions.comment",
                "is.workflow.actions.alert"
                ]:
                continue
            APINameList.append(WFWorkflowActionIdentifier)

        APINameList = list(set(APINameList))
        for j, APIName in enumerate(APINameList):
            APIDescription = all_api2info[APIName]
            APIDescriptionList.append(APIDescription)
        
        """Preparing system_prompt and user_prompt"""
        system_prompt = SYSTEM_PROMPT_TEMPLATE
        user_prompt = USER_PROMPT_TEMPLATE.format(
            RecordName=RecordName, 
            DescriptionoftheShortcutWorkflow=DescriptionoftheShortcutWorkflow, 
            Comments=Comments, 
            DescriptionInStore=DescriptionInStore, 
            APIDescriptionList="\n".join(APIDescriptionList))

        def num_tokens_from_string(string: str, encoding_name: str) -> int:
            encoding = tiktoken.get_encoding(encoding_name)
            num_tokens = len(encoding.encode(string))
            return num_tokens

        token_count = num_tokens_from_string(system_prompt + user_prompt, "cl100k_base")
        if token_count > 100000:
            print(f"Fail! Token count exceeds 100000! generating shortcut {URL} for {RecordName}")
            generated_fail_queries[URL] = {
                "TokenCount": token_count,
                "RecordName": RecordName,
                "DescriptionInStore": DescriptionInStore,
                "DescriptionoftheShortcutWorkflow": DescriptionoftheShortcutWorkflow,
                "Comments": Comments,
                "APIDescriptionList": APIDescriptionList
                }
            continue

        try:
            completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                )
            input_token_count += completion.usage.prompt_tokens
            output_token_count += completion.usage.completion_tokens

        except Exception as e:
            print(f"Fail! Generation Error! generating shortcut {URL} for {RecordName}")
            print(e)
            generated_fail_queries[URL] = {"Exception": str(e)}
            continue
        
        generated_content = None
        try:
            generated_content = completion.choices[0].message.content
            generated_content = {"GeneratedQuery" : json.loads(generated_content)}
            generated_success_queries[URL] = generated_content

            generated_success_queries[URL]["RecordName"] = RecordName
            generated_success_queries[URL]["DescriptionInStore"] = DescriptionInStore
            generated_success_queries[URL]["DescriptionoftheShortcutWorkflow"] = DescriptionoftheShortcutWorkflow
            generated_success_queries[URL]["Comments"] = Comments
            generated_success_queries[URL]["APIDescriptionList"] = APIDescriptionList

            print(f"Success! generating shortcut {URL} for {RecordName}")
            print(json.dumps(generated_success_queries[URL]["GeneratedQuery"], indent=4, ensure_ascii=False))

        except Exception as e:
            print(f"Fail! Parse Error! generating shortcut {URL} for {RecordName}")
            print(e)
            print(json.dumps(generated_content, indent=4, ensure_ascii=False))
            
            generated_fail_queries[URL] = {
                "RecordName": RecordName,
                "DescriptionInStore": DescriptionInStore,
                "DescriptionoftheShortcutWorkflow": DescriptionoftheShortcutWorkflow,
                "Comments": Comments,
                "APIDescriptionList": APIDescriptionList,
                "Exception": str(e), 
                "completion": generated_content
            }
            continue
        
        input_cost = input_token_count / 1000000 * input_price_every_million
        output_cost = output_token_count / 1000000 * output_price_every_million
        total_cost = input_cost + output_cost
        print(f"Token count: {input_token_count}, {output_token_count}, Input Cost {input_cost}, Output Cost {output_cost}, Total Cost {total_cost}")
        time.sleep(1)

        # Save every 100 entries.
        cnt += 1
        if cnt % 10 == 0:
            with open(os.path.join("./", "cost.json"), "w") as f:
                json.dump({"input_token_count": input_token_count, "output_token_count": output_token_count, "input_cost": input_cost, "output_cost": output_cost, "total_cost": total_cost}, f, indent=4, ensure_ascii=False)

            print(f"Saving successful results... Entry {cnt}.")
            generated_success_path = os.path.join(SHORTCUT_DATA, "tmp", f"generated_success_queries.json")
            with open(generated_success_path, "w") as f:
                json.dump(generated_success_queries, f, ensure_ascii=False, indent=4)

            print(f"Saving failed results... Entry {cnt}.")   
            generated_fail_path = os.path.join(SHORTCUT_DATA, "tmp", f"generated_fail_queries.json")
            with open(generated_fail_path, "w") as f:
                json.dump(generated_fail_queries, f, ensure_ascii=False, indent=4)

    with open(os.path.join("./", "cost.json"), "w") as f:
            json.dump({"input_token_count": input_token_count, "output_token_count": output_token_count, "input_cost": input_cost, "output_cost": output_cost, "total_cost": total_cost}, f, indent=4, ensure_ascii=False)

    print("Saving successful results...")
    generated_success_path = os.path.join(SHORTCUT_DATA, "tmp", "generated_success_queries.json")
    with open(generated_success_path, "w") as f:
        json.dump(generated_success_queries, f, indent=4, ensure_ascii=False)
    
    print("Saving failed results...")
    generated_fail_path = os.path.join(SHORTCUT_DATA, "tmp", "generated_fail_queries.json")
    with open(generated_fail_path, "w") as f:
        json.dump(generated_fail_queries, f, indent=4, ensure_ascii=False)

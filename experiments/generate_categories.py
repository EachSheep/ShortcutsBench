"""Generate descriptions and categories for shortcuts with action lengths ≤ 30.

Description: Briefly describe the functionality of the shortcut.
Category: One of the eight main categories.
"""

import json
import os
import time
import sys
import openai
import tiktoken
from generate_shortcut_desc import WFActionsClass, APIsClass

SHORTCUT_DATA = os.getenv("SHORTCUT_DATA", "")
if SHORTCUT_DATA == "":
    raise Exception("The `SHORTCUT_DATA` environment variable is not set.")

sys.path.append(SHORTCUT_DATA)

# Load the `cal_WFWorkflowActions_len` function from `cal_shortcut_len.py`.
from cal_shortcut_len import cal_WFWorkflowActions_len

client = openai.OpenAI()
model_name = "gpt-3.5-turbo"
input_price_every_million, output_price_every_million = 0.5, 1.5
# model_name = "gpt-4o"
# input_price_every_million, output_price_every_million = 5, 15

SYSTEM_PROMPT_TEMPLATE = """Shortcut consist of a sequence of actions, each is an API call, to execute user-provided queries. 

As a friendly and patient assistant, you need to categorize the provided shortcut into one of the following eight categories:
1. Productivity & Utilities
2. Health & Fitness
3. Entertainment & Media
4. Lifestyle & Social
5. Education & Reference
6. Business & Finance
7. Development & API
8. Home & Smart Devices

For each shortcut command, I will provide you with five fields:
1. 'RecordName': The name of the shortcut, briefly describing its function.
2. 'Description of the Shortcut Workflow': A description of the entire action workflow of the shortcut.
3. 'Comments': Optional. Notes from the shortcut's developer, which may describe its functions or other features.
4. 'Description in Store': A description of the shortcut’s functionality provided in the shortcut store.
5. 'API Description List': Detailed descriptions of the APIs involved in the shortcut.

You should rely primarily on the 'Description of the Shortcut Workflow' and 'API Description List', and refer to 'RecordName', 'Comments', and 'Description in Store' to give the final category.

The 'Description of the Shortcut Workflow' details the entire action workflow of the shortcut, with each line representing an API call. Each line is divided into five parts by semicolons:
1. The API's name.
2. A natural language description of the function performed by the API call, including parameter values presented as ${ParaName}=ParaValue.
3. Any additional parameters and their values required by the API call, which may not be mentioned in part 2.
4. The name of the API call's return value, which may be empty.
5. Specific parameter values that you must integrate into the query you generate, which may also be empty.

The 'API Description List' provides a comprehensive description of all APIs that can be invoked by the shortcut. This includes API name, parameter names, parameter types, parameter default values, parameter return value names, and return value types. Additionally, marked with Parameters for parameter names and explanations, Description for a brief and detailed API functionality description, and ParameterSummary for a natural language description of the API.
"""

USER_PROMPT_TEMPLATE = """Below are the five fields I provide to you:
1. 'RecordName': {RecordName}
2. 'Description of the Shortcut Workflow': {DescriptionoftheShortcutWorkflow}
3. 'Comments': {Comments}
4. 'Description in Store': {DescriptionInStore}
5. 'API Description List': {APIDescriptionList}

Please give the category on these details. Alongside the category, provide the shortcut's name and a description of its functionality in english using the following JSON format:
{{
    "category": "category", # The category must be in ['Productivity & Utilities', 'Health & Fitness', 'Entertainment & Media', 'Lifestyle & Social', 'Education & Reference', 'Business & Finance', 'Development & API', 'Home & Smart Devices']
    "english_name": "ThisIsShortcutName",
	"english_functionality": "ThisIsFunctionality"
}}

Do not output any other content; your response should only be in this JSON format. 

Output the JSON directly without using ```json XX``` to enclose it. Please give your answer in English.

Begin!
"""

input_token_count = 0
output_token_count = 0

if __name__ == "__main__":
    
    """Definition file from the Shortcuts app"""
    WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "WorkflowKit.framework/Versions/A/Resources/WFActions.json")
    wf_actions_instance = WFActionsClass(WFActions_path)
    my_WFActions_path = os.path.join(SHORTCUT_DATA, "is.workflow.actions", "my_WFActions.json")
    wf_actions_instance.WFActions_dicts.update(json.load(open(my_WFActions_path, "r")))
    all_api2info_WF, _, _ = wf_actions_instance.all_api2desc(need_api2paraname2paratype=True, need_api2parasummary=True)

    """Load the definition file from the app"""
    # succ_api_json_path = os.path.join(SHORTCUT_DATA, "4_success_api_json_filter.json")
    # fail_api_json_path = os.path.join(SHORTCUT_DATA, "4_fail_api_json_filter.json")
    # API_instance = APIsClass(succ_api_json_path, fail_api_json_path)
    api_json_path = os.path.join(SHORTCUT_DATA, "4_api_json_filter.json")
    API_instance = APIsClass(api_json_path)
    all_api2info_from_app, _, _ = API_instance.all_api2desc(need_api2paraname2paratype=True, need_api2parasummary=True)
    """Mapping of all APIs to their description files"""
    all_api2info = all_api2info_WF.copy()
    all_api2info.update(all_api2info_from_app)
    # print(len(all_api2info_WF), len(all_api2info_from_app), len(all_api2info))

    final_detailed_records_path = os.path.join(SHORTCUT_DATA, "1_final_detailed_records_filter_apis_leq_30.json")
    with open(final_detailed_records_path, "r") as rp:
        final_detailed_records = json.load(rp)
    # Sort `final_detailed_records` in descending order based on the results of the `cal_WFWorkflowActions_len` function.
    final_detailed_records.sort(key=lambda x: cal_WFWorkflowActions_len(x["shortcut"]["WFWorkflowActions"], URL=x["URL"]), reverse=True)

    """Mapping of shortcut URLs to shortcut descriptions"""
    with open(os.path.join(SHORTCUT_DATA, "shortcut2desc.json"), "r") as fp:
        shortcut2desc = json.load(fp)
    
    generated_success_path = os.path.join(SHORTCUT_DATA, f"generated_success_categories.json")
    if os.path.exists(generated_success_path):
        with open(generated_success_path, "r") as f:
            generated_success_categories = json.load(f)
    else:
        generated_success_categories = {}
    generated_fail_path = os.path.join(SHORTCUT_DATA, f"generated_fail_categories.json")
    if os.path.exists(generated_fail_path):
        with open(generated_fail_path, "r") as f:
            generated_fail_categories = json.load(f)
    else:
        generated_fail_categories = {}

    cnt = 0
    for i, cur_shortcut in enumerate(final_detailed_records):
        URL = cur_shortcut["URL"]
        print(f"Generating query for shortcut {i + 1}... {URL}. {len(final_detailed_records) - len(generated_success_categories)} shortcuts remaining.")

        if URL in generated_success_categories:
            continue

        shortcut = cur_shortcut["shortcut"]
        if shortcut is None:
            continue
        
        NameINStore = cur_shortcut["NameINStore"][0]
        RecordName = cur_shortcut["records"]["fields"]["name"]["value"]
        DescriptionInStore = cur_shortcut["DescriptionInStore"][0]
        if URL not in shortcut2desc:
            print(f"Fail! No description for shortcut {URL} for {RecordName}")
            continue
        DescriptionoftheShortcutWorkflow = shortcut2desc[URL]
        Comments = None
        APINameList, APIDescriptionList = [], []

        WFWorkflowActions = shortcut["WFWorkflowActions"]
        for WFWorkflowAction in WFWorkflowActions[:1]: # Only include the content of the first comment.
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
        
        """Prepare `system_prompt` and `user_prompt`."""
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
            generated_fail_categories[URL] = {
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
                    ]
                )
            input_token_count += completion.usage.prompt_tokens
            output_token_count += completion.usage.completion_tokens

        except Exception as e:
            print(f"Fail! Generation Error! generating shortcut {URL} for {RecordName}")
            print(e)
            generated_fail_categories[URL] = {"Exception": str(e)}
            continue
        
        generated_content = None
        try:
            generated_content = completion.choices[0].message.content
            generated_content = json.loads(generated_content)
            generated_success_categories[URL] = generated_content

            print(f"Success! generating shortcut {URL} for {RecordName}")
            print(json.dumps(generated_success_categories[URL], indent=4, ensure_ascii=False))

        except Exception as e:
            print(f"Fail! Parse Error! generating shortcut {URL} for {RecordName}")
            print(e)
            print(json.dumps(generated_content, indent=4, ensure_ascii=False))
            
            generated_fail_categories[URL] = {}
            continue
        
        input_cost = input_token_count / 1000000 * input_price_every_million
        output_cost = output_token_count / 1000000 * output_price_every_million
        total_cost = input_cost + output_cost
        print(f"Token count: {input_token_count}, {output_token_count}, Input Cost {input_cost}, Output Cost {output_cost}, Total Cost {total_cost}")
        time.sleep(1)

        # Save every 100 entries.
        cnt += 1
        if cnt % 100 == 0:
            # with open(os.path.join(SHORTCUT_DATA, "cost_generate_categories.json"), "w") as f:
            #     json.dump({"input_token_count": input_token_count, "output_token_count": output_token_count, "input_cost": input_cost, "output_cost": output_cost, "total_cost": total_cost}, f, indent=4, ensure_ascii=False)

            print(f"Saving successful results... Entry {cnt}")
            generated_success_path = os.path.join(SHORTCUT_DATA, f"generated_success_categories.json")
            # with open(generated_success_path, "w") as f:
            #     json.dump(generated_success_categories, f, ensure_ascii=False, indent=4)

            print(f"Saving failed results... Entry {cnt}")   
            generated_fail_path = os.path.join(SHORTCUT_DATA, f"generated_fail_categories.json")
            # with open(generated_fail_path, "w") as f:
            #     json.dump(generated_fail_categories, f, ensure_ascii=False, indent=4)

    # with open(os.path.join(SHORTCUT_DATA, "cost_generate_categories.json"), "w") as f:
    #     json.dump({"input_token_count": input_token_count, "output_token_count": output_token_count, "input_cost": input_cost, "output_cost": output_cost, "total_cost": total_cost}, f, indent=4, ensure_ascii=False)

    print("Saving successful results...")
    generated_success_path = os.path.join(SHORTCUT_DATA, "generated_success_categories.json")
    # with open(generated_success_path, "w") as f:
    #     json.dump(generated_success_categories, f, indent=4, ensure_ascii=False)
    
    print("Saving failed results...")
    generated_fail_path = os.path.join(SHORTCUT_DATA, "generated_fail_categories.json")
    # with open(generated_fail_path, "w") as f:
    #     json.dump(generated_fail_categories, f, indent=4, ensure_ascii=False)

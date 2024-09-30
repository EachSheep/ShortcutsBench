"""
Test Experiment: Evaluate the ability to select the correct API, without assessing parameters.
"""

import json
import os
import random
import time
import re
import openai
import copy
import logging
import argparse

from other_prompt import SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE

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

    def set_history_actions(self, history_actions): # TODO
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

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--model_name", type=str, default=None)  # Model name
    argparser.add_argument("--dataset_name", type=str, default=None)  # dataset name
    argparser.add_argument("--sample_num", type=int, default=0)
    args = argparser.parse_args()
    
    # SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_OTHER_DATA")
    if args.dataset_name == "metatool":
        SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_METATOOL_OTHER_DATA")
    elif args.dataset_name == "toolbench":
        SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLBENCH_OTHER_DATA")
    elif args.dataset_name == "toolllm":
        SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLLLM_OTHER_DATA")
    else:
        raise ValueError("args.dataset_name error")

    use_openai_style = False  # Use OpenAI's style

    if args.model_name in [
        "gpt-4o-mini",
    ]:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = openai.OpenAI()
        create_completion_client = client.chat.completions.create

        if args.model_name == "gpt-4o-mini":
            input_price_every_million, output_price_every_million = 0.15, 0.6
        else:
            raise Exception("args.model_name error")
        use_openai_style = True
    elif args.model_name in [
        "qwen2:0.5b-instruct-fp16",
        "qwen2:1.5b-instruct-fp16",
        "qwen2:7b-instruct-fp16",
        "qwen2.5:0.5b-instruct-fp16",
        "qwen2.5:1.5b-instruct-fp16",
        "qwen2.5:3b-instruct-fp16",
        "qwen2.5:7b-instruct-fp16",
        "gemma2:2b-instruct-fp16",
        "gemma2:9b-instruct-fp16",
        "llama3:8b-instruct-fp16",
        "llama3.1:8b-instruct-fp16",
        "llama3.2:3b-instruct-fp16"
    ]:
        OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
        OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
        client = openai.OpenAI(
            base_url = OLLAMA_BASE_URL,
            api_key=OLLAMA_API_KEY, # required, but unused
        )
        create_completion_client = client.chat.completions.create

        input_price_every_million, output_price_every_million = 0., 0.
        use_openai_style = True
    else:
        raise NotImplementedError

    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)
    if not os.path.exists('log'):
        os.makedirs('log')
    file_handler = logging.FileHandler(
        f'log/experiment_{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.log')
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

    logger.info(f"args.model_name: {args.model_name}")

    # Get the query.
    generated_success_queries_path = os.path.join(
        SHORTCUTSBENCH_OTHER_DATA, "generated_success_queries.json")
    with open(generated_success_queries_path, "r") as f:
        generated_success_queries = json.load(f)
    logger.info(f"Number of queries: {len(generated_success_queries)}")

    # Slashes (/) in `args.model_name` will be replaced with underscores (_).
    path_model_name = args.model_name.replace("/", "_")
    res_path = os.path.join(SHORTCUTSBENCH_OTHER_DATA, 
                            # Path to store the final agent-generated results
                            f"experiment_res_{path_model_name}.jsonl")
    already_processed_queries_list = []  # Final saved experimental results
    if os.path.exists(res_path):
        with open(res_path, "r") as f:
            already_processed_queries_list = [
                json.loads(line) for line in f.readlines()]
    already_processed_set = set(
        [res["URL"] for res in already_processed_queries_list])  # Processed queries will not be reprocessed.
    del already_processed_queries_list

    to_be_processed_num = len(generated_success_queries) - len(already_processed_set)
    logger.info(f"Number of processed queries: {len(already_processed_set)}. Number of remaining queries: {to_be_processed_num}")
    
    # Randomly shuffle `generated_success_queries`.
    generated_success_queries = dict(random.sample(list(generated_success_queries.items()), len(generated_success_queries)))

    if args.sample_num:
        generated_success_queries = dict(random.sample(list(generated_success_queries.items()), args.sample_num))
        logger.info(f"Sampled {args.sample_num} shortcuts.")
    
    all_api2info_path = os.path.join(SHORTCUTSBENCH_OTHER_DATA, "all_api2info.json")
    with open(all_api2info_path, "r") as f:
        all_api2info = json.load(f)

    new_res_list = []  # Store the new experimental results.
    logger.info("Begin processing new shortcuts.")
    cnt = 0  # Number of new shortcuts processed this times
    # for URL, cur_query_dict in random_200_success_queries.items():
    for URL, cur_query_dict in generated_success_queries.items():

        if URL in already_processed_set:  # Queries that have already been processed will not be reprocessed.
            continue

        logger.info(f"Processing {URL}, {cnt}/{to_be_processed_num}= {cnt / to_be_processed_num * 100:.2f}")

        query = cur_query_dict["query"]
        action_seqs = cur_query_dict["action_seqs"]
        logger.info(f"The current query is: {query}")

        unique_identifies = []
        for cur_action in action_seqs:
            api_name = cur_action["api_name"]
            unique_identifies.append(api_name)
        unique_identifies = list(set(unique_identifies)) # Retrieve all `cur_identifier` for the current query.
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

        log_query = query
        log_api_descs = input_API_descs  # Each query has multiple available APIs, represented as a dictionary mapping API names to API descriptions.
        log_api_names = input_API_names  # Each query has multiple available APIs, represented as a list of API names.
        aseqs = action_seqs
        tmp_aseqs = []  # Each query has multiple actions, corresponding one-to-one with the standard answers. This list does not include actions from `filter_WFWorkflowActionIdentifier_list`.
        bseqs = []  # Each query has multiple actions, corresponding one-to-one with the standard answers. This list includes actions from `filter_WFWorkflowActionIdentifier_list` and should be stored.
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            all_api_descs=agent_instance.all_api_descs,
            all_api_names=agent_instance.all_api_names,
        )
        # print("system_prompt:", system_prompt)
        # input()

        context_length_exceeded_error = False
        for aseq in aseqs:

            api_name = copy.deepcopy(aseq["api_name"])
            api_action = copy.deepcopy(aseq["api_action"])
            api_reaction = copy.deepcopy(aseq["api_reaction"])

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
                            model=args.model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ]
                        )
                        break

                    except Exception as e:
                        print(f"Fail! Generation Error! generating action for {URL}")
                        print(e)

                        # If `context_length_exceeded` appears in `str(e)`.
                        if "context_length_exceeded" in str(e):  # chatgpt
                            context_length_exceeded_error = True
                            break
                        elif "Range of input length should be" in str(e):
                            context_length_exceeded_error = True
                            break
                        elif "Input validation error" in str(e):
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
                        cur_try_time += 1
                        time.sleep(1)

                        if cur_try_time == save_try_times:
                            # Save the current result.
                            print(f"Processed {cnt} results.")
                            path_model_name = args.model_name.replace("/", "_")
                            res_path = os.path.join(
                                SHORTCUTSBENCH_OTHER_DATA, f"experiment_res_{path_model_name}.jsonl")
                            with open(res_path, "a") as f:
                                write_str = ""
                                for res in new_res_list:
                                    write_str += json.dumps(res,
                                                            ensure_ascii=False) + "\n"
                                f.write(write_str)

                            new_res_list = []

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
                else:
                    raise ValueError("No style is used.")
                generated_content = json.loads(generated_content)
            except Exception as e:
                print(f"Fail! Parse Error! generating action for {URL}")
                print(e)

                bseqs.append(
                    {"state": "json_error", "aseq": generated_content})
                tmp_aseqs.append({
                        "api_name": api_name,
                        "api_action": api_action,
                        "api_reaction": api_reaction,
                    })  # Prepare for the next prediction.
                time.sleep(0.5)
                continue

            bseqs.append({"state": "generated_by_agent",
                            "aseq": generated_content})
            tmp_aseqs.append({
                    "api_name": api_name,
                    "api_action": api_action,
                    "api_reaction": api_reaction
                })  # Prepare for the next prediction.

            time.sleep(0.5)

        if len(aseqs) != len(bseqs):
            res_aseqs = aseqs[:len(bseqs)]
        else:
            res_aseqs = aseqs

        new_res_list.append({
            "URL": URL,
            "query": log_query,
            "api_names": log_api_names,
            "api_descs": log_api_descs,
            "aseqs": res_aseqs,
            "bseqs": bseqs,
        })

        cnt += 1
        logger.info(f"Processed {cnt} results.")
        if cnt % 10 == 0:  # Save every 10 entries.

            logger.info(f"Saving {cnt} results.")
            path_model_name = args.model_name.replace("/", "_")
            res_path = os.path.join(
                SHORTCUTSBENCH_OTHER_DATA, f"experiment_res_{path_model_name}.jsonl")
            with open(res_path, "a") as f:
                write_str = ""
                for res in new_res_list:
                    write_str += json.dumps(res, ensure_ascii=False) + "\n"
                f.write(write_str)

            new_res_list = []
            logger.info(f"Saved {cnt} results.")

    logger.info(f"Finish processing {cnt} results.")

    if new_res_list:
        
        path_model_name = args.model_name.replace("/", "_")
        cost_path = os.path.join(
            SHORTCUTSBENCH_OTHER_DATA, f"experiment_cost_{path_model_name}.jsonl")

        path_model_name = args.model_name.replace("/", "_")
        res_path = os.path.join(
            SHORTCUTSBENCH_OTHER_DATA, f"experiment_res_{path_model_name}.jsonl")
        with open(res_path, "a") as f:
            write_str = ""
            for res in new_res_list:
                write_str += json.dumps(res, ensure_ascii=False) + "\n"
            f.write(write_str)

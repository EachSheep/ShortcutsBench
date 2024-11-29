"""
Since smaller models like 7B have limited instruction-following capabilities, they often fail to produce outputs in the required format when prompted.

To address this, I need to use an additional model to convert their outputs into the desired format, making evaluation more convenient.
"""

import argparse
import json
import os
import openai
from multiprocessing import Pool, cpu_count

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()
create_completion_client = client.chat.completions.create
SHORTCUT_DATA_FOR_AGENT_LLM_ORIGIN = os.getenv("SHORTCUT_DATA_FOR_AGENT_LLM_ORIGIN")

def read_jsonl_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        return [json.loads(line.strip()) for line in infile if line.strip()]

# def write_jsonl_file(output_file, data):
#     with open(output_file, 'w', encoding='utf-8') as outfile:
#         for item in data:
#             json_line = json.dumps(item, ensure_ascii=False)
#             outfile.write(json_line + '\n')

def write_jsonl_file(output_file, data):
    with open(output_file, 'w', encoding='utf-8', errors='replace') as outfile:
        for item in data:
            try:
                json_line = json.dumps(item, ensure_ascii=False)
                outfile.write(json_line + '\n')
            except UnicodeEncodeError as e:
                print(f"UnicodeEncodeError while processing item: {item}")
                print(f"Error details: {e}")

def correct_json_error_in_bseqs(entry, model_name='gpt-4o-mini'):
    bseqs = entry.get('bseqs', [])
    for i, bseq_entry in enumerate(bseqs):
        state = bseq_entry.get('state', '')
        if state == 'json_error':
            corrected_aseq = correct_aseq(bseq_entry['aseq'], model_name)
            if corrected_aseq:
                bseq_entry['aseq'] = corrected_aseq
                bseq_entry['state'] = 'corrected_by_model'
            else:
                print(f"Failed to correct bseq entry at index {i}")
    return entry

def correct_aseq(aseq, model_name):
    # Construct the prompts
    system_prompt = construct_system_prompt()
    user_prompt = construct_user_prompt(aseq)

    # Call the OpenAI API
    try:
        response = create_completion_client(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0  # Using 0 for deterministic output
        )
        corrected_output = response.choices[0].message.content.strip()
        # Validate the corrected output
        corrected_json = json.loads(corrected_output)
        return corrected_json
    except Exception as e:
        print(f"Error correcting aseq: {e}")
        return None

def construct_system_prompt():
    # Define the correct JSON format and provide examples
    system_prompt = (
        "You are an assistant that helps correct JSON outputs into the required format.\n"
        "The required JSON format for 'aseq' is as follows:\n\n"
        "{\n"
        '    "WFWorkflowActionIdentifier": String,\n'
        '    "WFWorkflowActionParameters": {\n'
        '        ParameterName: ParameterValue,\n'
        '        ...\n'
        '    }\n'
        "}\n\n"
        "An example of a correct 'aseq':\n"
        '{\n'
        '    "WFWorkflowActionIdentifier": "is.workflow.actions.searchweb",\n'
        '    "WFWorkflowActionParameters": {\n'
        '        "WFSearchWebDestination": "Google",\n'
        '        "WFInputText": "What are the best hiking trails in California?"\n'
        '    }\n'
        '}\n\n'
        "Please correct the provided 'aseq' to match this format, ensuring all necessary fields are present "
        "and properly structured. Do not include any explanations or extra content—just provide the corrected JSON."
        "If you encounter a truncated JSON where a parameter’s value is incomplete, such as '{\"operation\": \"turn\", \"state\":\"，', retain the complete parameter (e.g., \"operation\") and remove the incomplete one (e.g., \"state\")."
    )
    return system_prompt

def construct_user_prompt(aseq):
    user_prompt = (
        f"The following 'aseq' has errors in its format:\n\n{aseq}\n\n"
        "Please correct it to match the required JSON format for 'aseq' as described."
    )
    return user_prompt

def process_entries(entries, output_entries, model_name):
    print("Processing entries...")
    processed_entries = []
    URL_2_output_entries = {entry['URL']: entry for entry in output_entries}
    for idx, entry in enumerate(entries):
        print(f"Processing entry {idx + 1} of {len(entries)}...")
        URL = entry.get('URL', '')
        if URL in URL_2_output_entries:
            output_entry = URL_2_output_entries[URL]
            processed_entries.append(output_entry)
        else:
            corrected_entry = correct_json_error_in_bseqs(entry, model_name)
            processed_entries.append(corrected_entry)
    print("Finished processing all entries.")
    return processed_entries

def process_single_entry(args):
    """Wrapper for processing a single entry to be used in multiprocessing."""
    entry, model_name = args
    return correct_json_error_in_bseqs(entry, model_name)

def process_entries_parallel(entries, model_name, num_workers):
    print("Processing entries in parallel...")
    num_workers = min(num_workers, len(entries))  # Limit workers to available CPUs or the number of entries
    with Pool(processes=num_workers) as pool:
        # Map each entry along with model_name as an argument tuple
        processed_entries = pool.map(process_single_entry, [(entry, model_name) for entry in entries])
    print("Finished processing all entries in parallel.")
    return processed_entries

def main():
    parser = argparse.ArgumentParser(description='Process jsonl files to correct JSON errors in bseqs.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input jsonl file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output jsonl file.')
    parser.add_argument('--num_workers', type=int, help='Number of workers for parallel processing.')
    args = parser.parse_args()

    args.input_file = os.path.join(SHORTCUT_DATA_FOR_AGENT_LLM_ORIGIN, args.input_file)
    args.output_file = os.path.join(SHORTCUT_DATA_FOR_AGENT_LLM_ORIGIN, args.output_file)

    # Read the input file
    entries = read_jsonl_file(args.input_file)
    if os.path.exists(args.output_file):
        output_entries = read_jsonl_file(args.output_file)
    else:
        output_entries = []

    # Process the entries
    processed_entries = process_entries(entries, output_entries, model_name='gpt-4o-mini')
    # Process the entries using parallel processing
    # processed_entries = process_entries_parallel(entries, model_name='gpt-4o-mini', num_workers=args.num_workers)

    # Write the output file
    write_jsonl_file(args.output_file, processed_entries)

if __name__ == '__main__':
    main()
import json
import os
import argparse
import re

# Parse command-line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("--model_name", type=str, default=None)  # Model name
argparser.add_argument("--dataset_name", type=str, default=None)  # Dataset name
argparser.add_argument("--sample_num", type=int, default=0)  # Sample number (if needed)
argparser.add_argument("--delete_json_error", action="store_true", default=False)
args = argparser.parse_args()

# Set the path for the correct dataset based on the dataset_name
if args.dataset_name == "metatool":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_METATOOL_OTHER_DATA")
elif args.dataset_name == "toolbench":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLBENCH_OTHER_DATA")
elif args.dataset_name == "toolllm":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLLLM_OTHER_DATA")
elif args.dataset_name == "toollens":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLLENS_OTHER_DATA")
else:
    raise ValueError("Invalid dataset_name provided")

# Prepare the result path for the experiment file
path_model_name = args.model_name.replace("/", "_")
res_path = os.path.join(SHORTCUTSBENCH_OTHER_DATA, 
                        f"pre_experiment_res_{path_model_name}.jsonl")

# Variables for tracking accuracy
total_count = 0
correct_count = 0
mismatches = []  # To store information about mismatched queries

None_num = 0

# Open and read the JSONL file
with open(res_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)  # Parse each line as JSON
        
        # Extract api_name from aseqs and bseqs
        aseq_api_name = data['aseqs'][0]['api_name'] if 'aseqs' in data and data['aseqs'] else None
        try:
            bseq_api_name = data['bseqs'][0]['aseq']['api_name'] if 'bseqs' in data and data['bseqs'] else None
        except:
            # Extract the value of api_name using regular expressions.
            json_str = data['bseqs'][0]['aseq']
            if isinstance(json_str, str):
                pattern = r'"api_name":\s*(?:"([^"]+)"|([^\s,}]+))' # Match values enclosed in quotes or values without quotes
                match = re.search(pattern, json_str)

                if match:
                    bseq_api_name = match.group(1) if match.group(1) else match.group(2)
                else:
                    bseq_api_name = None
            else:
                bseq_api_name = None
            
            if bseq_api_name is None:
                # print(data['bseqs'])
                None_num += 1
                continue
        try:
            if '[' in bseq_api_name:
                bseq_api_name = bseq_api_name.split("[")[0] # Only the function name, not the passed arguments
        except:
            print(bseq_api_name)
            # exit(1)
        
        # Compare the api_name from aseq and bseq
        if aseq_api_name == bseq_api_name:
            correct_count += 1
        else:
            # If they don't match, collect the query and both api_name details for reporting
            mismatches.append({
                'query': data['query'],
                'aseq_api_name': aseq_api_name,
                'bseq_api_name': bseq_api_name
            })
        
        total_count += 1

# Calculate accuracy
accuracy = correct_count / total_count if total_count > 0 else 0

# If there are mismatches, print the details in a friendly format
if mismatches:
    print("\nMismatched Queries and API Names:")
    for mismatch in mismatches:
        print(f"Query: {mismatch['query']}")
        print(f"  aseq API Name: {mismatch['aseq_api_name']}")
        print(f"  bseq API Name: {mismatch['bseq_api_name']}")
        print("-" * 40)
else:
    print("All queries matched successfully!")

# Print accuracy result
print(f"Accuracy: {accuracy:.4f}, None_num: {None_num}")
print(f'correct_count: {correct_count}, total_count: {total_count}')
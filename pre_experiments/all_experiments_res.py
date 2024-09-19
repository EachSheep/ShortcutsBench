import json
import os
import argparse

# Parse command-line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("--model_name", type=str, default=None)  # Model name
argparser.add_argument("--dataset_name", type=str, default=None)  # Dataset name
argparser.add_argument("--sample_num", type=int, default=0)  # Sample number (if needed)
args = argparser.parse_args()

# Set the path for the correct dataset based on the dataset_name
if args.dataset_name == "metatool":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_METATOOL_OTHER_DATA")
elif args.dataset_name == "toolbench":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLBENCH_OTHER_DATA")
elif args.dataset_name == "toolllm":
    SHORTCUTSBENCH_OTHER_DATA = os.getenv("SHORTCUTSBENCH_TOOLLLM_OTHER_DATA")
else:
    raise ValueError("Invalid dataset_name provided")

# Prepare the result path for the experiment file
path_model_name = args.model_name.replace("/", "_")
res_path = os.path.join(SHORTCUTSBENCH_OTHER_DATA, 
                        f"experiment_res_{path_model_name}.jsonl")

# Variables for tracking accuracy
total_count = 0
correct_count = 0
mismatches = []  # To store information about mismatched queries

# Open and read the JSONL file
with open(res_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)  # Parse each line as JSON
        
        # Extract api_name from aseqs and bseqs
        aseq_api_name = data['aseqs'][0]['api_name'] if 'aseqs' in data and data['aseqs'] else None
        bseq_api_name = data['bseqs'][0]['aseq']['api_name'] if 'bseqs' in data and data['bseqs'] else None
        
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
print(f"Accuracy: {accuracy:.4f}")
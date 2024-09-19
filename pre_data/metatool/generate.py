import json
import uuid
import pandas as pd
import argparse
import random

# Define the function to handle sampling and JSON generation
def generate_json_files(sample_size):
    # Load the data from multi_tool_query_golden.json
    with open('multi_tool_query_golden.json', 'r') as f:
        multi_tool_query_golden = json.load(f)

    # Load the data from all_clean_data.csv
    all_clean_data = pd.read_csv('all_clean_data.csv')

    # Prepare a list to combine both data sources for sampling
    queries = []
    query_tools = []

    # Add queries and their tools from multi_tool_query_golden.json
    for entry in multi_tool_query_golden:
        queries.append(entry['query'])
        query_tools.append(entry['tool'])

    # Add queries and their tools from all_clean_data.csv
    queries.extend(all_clean_data['Query'].tolist())
    query_tools.extend(all_clean_data['Tool'].apply(lambda x: [x]).tolist())  # Ensure tools are in list format

    # Combine queries and tools into a list of tuples
    combined_data = list(zip(queries, query_tools))

    # Shuffle the combined data to ensure random sampling
    random.shuffle(combined_data)

    # Sample 'sample_size' number of queries (if less, repeat to reach the required size)
    sampled_data = combined_data * (sample_size // len(combined_data)) + combined_data[:sample_size % len(combined_data)]

    # Generate the 'generated_success_queries.json' structure
    generated_success_queries = {}

    for query, tools in sampled_data:
        unique_id = str(uuid.uuid4())  # Generate unique id for each query
        generated_success_queries[unique_id] = {
            "query": query,
            "action_seqs": [
                {
                    "api_name": tool,  # Set the tool as api_name
                    "api_action": None,
                    "api_reaction": None
                } for tool in tools
            ]
        }

    # Create all_api2info.json based on plugin_des.json
    with open('plugin_des.json', 'r') as f:
        plugin_des = json.load(f)

    # Generate the 'all_api2info.json' structure
    all_api2info = {api: description for api, description in plugin_des.items()}

    # Saving both JSONs to files
    with open("generated_success_queries.json", "w") as f:
        json.dump(generated_success_queries, f, indent=4)

    with open("all_api2info.json", "w") as f:
        json.dump(all_api2info, f, indent=4)

    print("Generated files are ready for download as 'generated_success_queries.json' and 'all_api2info.json'.")

if __name__ == "__main__":
    # Argument parsing for command-line sample size input
    parser = argparse.ArgumentParser(description="Generate JSON files for API queries.")
    parser.add_argument("--sample_size", type=int, help="The number of queries to sample and include in the output.")
    args = parser.parse_args()

    # Generate the JSON files with the provided sample size
    generate_json_files(args.sample_size)
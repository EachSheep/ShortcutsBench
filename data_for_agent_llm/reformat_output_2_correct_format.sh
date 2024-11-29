#!/bin/bash

# Define arrays of input and output files
INPUT_FILES=(
    # "experiment_res_THUDM_agentlm-7b.jsonl"
    # "experiment_res_THUDM_agentlm-13b.jsonl"
    # "experiment_res_THUDM_agentlm-70b.jsonl"
    # "experiment_res_Salesforce_xLAM-7b-r.jsonl"
    "experiment_res_Salesforce_xLAM-8x7b-r.jsonl"
    # "experiment_res_Salesforce_xLAM-8x7b-r.4k.jsonl"
    # "experiment_res_lemur-70b-chat-v1.jsonl"
)
OUTPUT_FILES=(
    # "experiment_res_THUDM_agentlm-7b.after_format.jsonl"
    # "experiment_res_THUDM_agentlm-13b.after_format.jsonl"
    # "experiment_res_THUDM_agentlm-70b.after_format.jsonl"
    # "experiment_res_Salesforce_xLAM-7b-r.after_format.jsonl"
    "experiment_res_Salesforce_xLAM-8x7b-r.after_format.jsonl"
    # "experiment_res_Salesforce_xLAM-8x7b-r.4k.after_format.jsonl"
    # "experiment_res_lemur-70b-chat-v1.after_format.jsonl"
)

num_workers=8

# Loop through each pair of input and output files
for ((i=0; i<${#INPUT_FILES[@]}; i++)); do
  INPUT_FILE=${INPUT_FILES[$i]}
  OUTPUT_FILE=${OUTPUT_FILES[$i]}
  
  python reformat_output_2_correct_format.py --input_file $INPUT_FILE --output_file $OUTPUT_FILE --num_workers $num_workers
done
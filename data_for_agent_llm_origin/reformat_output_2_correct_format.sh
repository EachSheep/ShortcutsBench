#!/bin/bash

# Define arrays of input and output files
INPUT_FILES=(
    # "experiment_res_meta-llama_Llama-2-7b-chat-hf.jsonl"
    # "experiment_res_meta-llama_Llama-2-13b-chat-hf.jsonl"
    # "experiment_res_mistralai_Mistral-7B-instruct-v0.1.jsonl"
    "experiment_res_mistralai_Mixtral-8x7B-Instruct-v0.1.jsonl"
)
OUTPUT_FILES=(
    # "experiment_res_meta-llama_Llama-2-7b-chat-hf.after_format.jsonl"
    # "experiment_res_meta-llama_Llama-2-13b-chat-hf.after_format.jsonl"
    # "experiment_res_mistralai_Mistral-7B-instruct-v0.1.after_format.jsonl"
    "experiment_res_mistralai_Mixtral-8x7B-Instruct-v0.1.after_format.jsonl"
)

num_workers=8

# Loop through each pair of input and output files
for ((i=0; i<${#INPUT_FILES[@]}; i++)); do
  INPUT_FILE=${INPUT_FILES[$i]}
  OUTPUT_FILE=${OUTPUT_FILES[$i]}
  
  python reformat_output_2_correct_format.py --input_file $INPUT_FILE --output_file $OUTPUT_FILE --num_workers $num_workers
done
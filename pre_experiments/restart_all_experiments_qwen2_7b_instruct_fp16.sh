#!/bin/bash

unset http_proxy
unset https_proxy

# Collect all parameters
ARGS=("$@")

# Define the base command
CMD="python all_experiments.py --model_name qwen2:7b-instruct-fp16"

# Check if --sample_num parameter is provided
for ((i=0; i < ${#ARGS[@]}; i++)); do
    if [[ ${ARGS[$i]} == --sample_num ]]; then
        SAMPLE_NUM=${ARGS[$((i+1))]}
        CMD="$CMD --sample_num $SAMPLE_NUM"
        break
    fi
done

# Check if --dataset_name parameter is provided
for ((i=0; i < ${#ARGS[@]}; i++)); do
    if [[ ${ARGS[$i]} == --dataset_name ]]; then
        DATASET_NAME=${ARGS[$((i+1))]}
        CMD="$CMD --dataset_name $DATASET_NAME"
        break
    fi
done

echo "CMD: $CMD"

# Infinite loop
while true; do
    # Execute the command
    $CMD
    # Output termination message
    echo "Program terminated, restarting..."
    # Pause before restarting; adjust as needed
    sleep 30
    break
done

#!/bin/bash

# Collect all parameters
ARGS=("$@")

# Define the basic command
CMD="python all_experiments.py --model_name deepseek-chat"

# Check if --sample_num argument is provided
for ((i=0; i < ${#ARGS[@]}; i++)); do
    if [[ ${ARGS[$i]} == --sample_num ]]; then
        SAMPLE_NUM=${ARGS[$((i+1))]}
        CMD="$CMD --sample_num $SAMPLE_NUM"
        break
    fi
done

echo "CMD: $CMD"

# Infinite loop
while true; do
    # Execute the command
    $CMD
    # Output program termination message
    echo "Program ended, restarting..."
    # Wait a few seconds before restarting, adjust as needed
    sleep 30
    break
done
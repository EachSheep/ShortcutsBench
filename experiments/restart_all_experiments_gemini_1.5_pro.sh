#!/bin/bash

# Collect all parameters
ARGS=("$@")

# Define the base command
CMD="python all_experiments.py --model_name gemini-1.5-pro"

# Check if --sample_num parameter is provided
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
    # Output termination message
    echo "Program terminated, restarting..."
    # Pause before restarting, adjust as needed
    sleep 30
    break
done

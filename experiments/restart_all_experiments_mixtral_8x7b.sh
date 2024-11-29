#!/bin/bash

# Collect all parameters
ARGS=("$@")

# Define the base command
CMD="python all_experiments.py --model_name mistralai/Mixtral-8x7B-instruct-v0.1"
# CMD="python all_experiments.py --model_name open-mixtral-8x7b"

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
    # Run the command
    $CMD
    # Output termination message
    echo "Program ended, restarting..."
    # Pause before restarting; adjust as needed
    sleep 30
    # Uncomment the following line to exit the loop after one iteration
    # break
done

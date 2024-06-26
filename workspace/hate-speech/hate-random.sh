#!/bin/bash

INPUT_FILE=$1
OUTPUT_FILE="out/hate-random.csv"

rm -rf "$OUTPUT_FILE"
touch "$OUTPUT_FILE"

if [ -z "$AMOUNT" ]; then
  echo "ERROR: AMOUNT is not set!"
  exit 1
fi

if [ -z "$INPUT_FILE" ]; then
  echo "ERROR: No input file defined!"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "ERROR: $INPUT_FILE does not exist!"
  exit 1
fi

shuf -n "$AMOUNT" "$INPUT_FILE" > "$OUTPUT_FILE"

echo "$AMOUNT lines of $INPUT_FILE were picked and copied to $OUTPUT_FILE"

import json
from loguru import logger
import argparse

VERSION = "v0.0.1"

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True)
parser.add_argument("-d", "--debug")
parser.add_argument("-v", "--version")
args = parser.parse_args()

# type: "spans", "logs" or "metrics"
def count_type(type, json_objects):
    count = 0
    for item in json_objects:
        formatted_type = f"resource{type.capitalize()}"

        # Found a match. Increment counter
        if formatted_type in item: count += 1

    return count

def start_program():
    with open(args.file, mode="r") as file:

        # As much as I'd like to read straight into JSON
        # Each line is a JSON object BUT
        # There are no commas
        # So read each line
        # And place in the array

        json_objects = []

        lines = file.readlines()
        for line in lines:
            # Remove whitespace and newlines from line
            line = line.strip()
            # Don't even try to interpret
            # We do not want to get into horrible bugs / security issues with interpretation and injection
            # Only add to array if line starts and ends with curly braces
            if line.startswith("{") and line.endswith("}"): json_objects.append(line)

        logger.info(f"Read {len(json_objects)} valid objects from file...")

        spans_count = count_type(type="spans", json_objects=json_objects)
        logger.info(f"File has {spans_count} spans...")
        logs_count = count_type(type="logs", json_objects=json_objects)
        logger.info(f"File has {logs_count} logs...")
        metrics_count = count_type(type="metrics", json_objects=json_objects)
        logger.info(f"File has {metrics_count} metrics...")

if __name__ == "__main__":
    start_program()

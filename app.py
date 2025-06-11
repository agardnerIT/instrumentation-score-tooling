import json
from loguru import logger
import argparse
import glob
import fnmatch

VERSION = "v0.0.1"
DEBUG_MODE = False

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True)
parser.add_argument("-d", "--debug")
parser.add_argument("-v", "--version")
args = parser.parse_args()

if args.debug:
    if (args.debug.lower() == "true" or
        args.debug.lower() == "t" or
        args.debug.lower() == "yes"):
        DEBUG_MODE = True

# type: "spans", "logs" or "metrics"
def count_type(type, json_objects):
    count = 0
    for item in json_objects:
        formatted_type = f"resource{type.capitalize()}"

        # Found a match. Increment counter
        if formatted_type in item: count += 1

    return count

def read_spec_rules():
    matching_files = glob.glob("spec/rules/*.md")

    # Remove the _template.md file
    current_pos = 0
    pos_to_remove = 0
    log_rules = []
    metric_rules = []
    resource_rules = []
    span_rules = []
    sdk_rules = []

    for file in matching_files:
        if file.endswith("_template.md"): pos_to_remove = current_pos
        current_pos += 1
        if "SPA" in file:
            span_rules.append(file)
        elif "LOG" in file:
            log_rules.append(file)
        elif "MET" in file:
            metric_rules.append(file)
        elif "RES" in file:
            resource_rules.append(file)
        elif "SDK" in file:
            sdk_rules.append(file)
    
    # Don't forget to remove _template.md
    matching_files.pop(pos_to_remove)

    return matching_files, span_rules, log_rules, metric_rules, resource_rules, sdk_rules


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

        if DEBUG_MODE:
            logger.info(f"Read {len(json_objects)} valid objects from file...")
            spans_count = count_type(type="spans", json_objects=json_objects)
            logger.info(f"File has {spans_count} spans...")
            logs_count = count_type(type="logs", json_objects=json_objects)
            logger.info(f"File has {logs_count} logs...")
            metrics_count = count_type(type="metrics", json_objects=json_objects)
            logger.info(f"File has {metrics_count} metrics...")

        all_rules, span_rules, log_rules, metric_rules, resource_rules, sdk_rules = read_spec_rules()
        
        if DEBUG_MODE:
            logger.info(f"Total rules: {len(all_rules)}")
            logger.info(f"Span rules: {len(span_rules)}")
            logger.info(f"Log rules: {len(log_rules)}")
            logger.info(f"Metric rules: {len(metric_rules)}")
            logger.info(f"Resource rules: {len(resource_rules)}")
            logger.info(f"SDK rules: {len(sdk_rules)}")


if __name__ == "__main__":
    start_program()

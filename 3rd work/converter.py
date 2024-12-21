import json
import argparse
import sys

def parse_value(value):
    if isinstance(value, dict):
        return parse_object(value)
    elif isinstance(value, list):
        return parse_array(value)
    else:
        return str(value)

def parse_object(obj):
    result = []
    for key, value in obj.items():
        result.append(f"{key} <- {parse_value(value)}")
    return "{\n" + "\n".join(result) + "\n}"

def parse_array(arr):
    result = []
    for item in arr:
        result.append(parse_value(item))
    return "#(" + ",\n".join(result) + ")"

def parse_json(data):
    result = []
    for key, value in data.items():
        result.append(f"{key} <- {parse_value(value)}")
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to configuration language.')
    parser.add_argument('input_file', help='Path to the input JSON file')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            data = json.load(f)
            output = parse_json(data)
            print(output)
    except FileNotFoundError:
        print(f"Error: File {args.input_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
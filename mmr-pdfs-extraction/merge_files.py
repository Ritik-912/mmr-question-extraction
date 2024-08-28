import argparse
import json
import glob
import pandas as pd

# Define the command-line arguments
parser = argparse.ArgumentParser(description='Merge JSON or CSV files in a folder')
parser.add_argument('-t', '--type', choices=['json', 'csv'], help='File type to merge')
parser.add_argument('-p', '--path', help='Folder path containing files to merge')

# Parse the command-line arguments
args = parser.parse_args()

# Get the file type and folder path from the arguments
file_type = args.type
folder_path = args.path

if file_type == 'json':
    # Merge JSON files
    json_files = glob.glob(folder_path + '/*.json')
    data = []
    for file in json_files:
        with open(file, 'r') as f:
            data.append(json.load(f))
    merged_data = []
    for file in json_files:
        with open(file, 'r') as f:
            merged_data.extend(json.load(f))
    with open('merged_file.json', 'w') as f:
        json.dump(merged_data, f, indent=4)
elif file_type == 'csv':
    # Merge CSV files
    csv_files = glob.glob(folder_path + '/*.csv')
    data = []
    for file in csv_files:
        data.append(pd.read_csv(file))
    merged_data = pd.concat(data, ignore_index=True)
    merged_data.to_csv('merged_file.csv', index=False)
else:
    print("Invalid file type. Please choose 'json' or 'csv'.")

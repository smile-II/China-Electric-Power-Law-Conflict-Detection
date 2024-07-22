import os
import json

# Define the sample structure for validation
sample_structure = {
    "office_level": str,
    "office": str,
    "effective_date": str,
    "publish_date": str,
    "status": str,
    "title": str,
    "chapter": str,
    "content": str
}

# Function to validate the structure of a single JSON object
def validate_json_structure(json_object, sample_structure):
    for key, value_type in sample_structure.items():
        if key not in json_object or not isinstance(json_object[key], value_type):
            return False
    return True

# Load the combined data
combined_file_path = 'data/raw_datasets/laws_zyp/combined_laws.json'
with open(combined_file_path, 'r', encoding='utf-8') as combined_file:
    combined_data = json.load(combined_file)

# Check the structure of each JSON object in the combined data
validation_results = [validate_json_structure(item, sample_structure) for item in combined_data]

# Check if all items have the correct structure
all_valid = all(validation_results)

all_valid


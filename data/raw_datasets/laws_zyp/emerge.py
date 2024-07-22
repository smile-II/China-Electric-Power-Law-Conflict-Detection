import os
import json

# Directory containing the files
directory_path = 'data/raw_datasets/laws_zyp/'

# Output file path
output_path = os.path.join(directory_path, 'combined_laws.json')

# Open the output file in write mode
with open(output_path, 'w', encoding='utf-8') as output_file:
    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json') and filename != 'combined_laws.json':
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    # Write each entry as a separate line in the output file
                    output_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"Combined data saved to {output_path}")

from datasets import load_dataset
import json
import pandas as pd
import numpy as np
import os

def convert_record(record):
    for key, value in record.items():
        if isinstance(value, (pd.Timestamp, np.datetime64)):
            record[key] = str(value)
    return record

# 下载并保存数据集的子集
def save_dataset_subset(dataset_name, subset_name, output_path):
    dataset = load_dataset(dataset_name, name=subset_name, split='train')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in dataset:
            record = convert_record(record)
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')
    print(f"子集 {subset_name} 已保存为 {output_path}")

# 指定数据集名称和子集名称
dataset_name = "twang2218/chinese-law-and-regulations"
subsets = ["default", "metadata"]
output_dir = "saved_datasets"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存数据集的不同子集
for subset in subsets:
    output_path = os.path.join(output_dir, f"{subset}.json")
    save_dataset_subset(dataset_name, subset, output_path)

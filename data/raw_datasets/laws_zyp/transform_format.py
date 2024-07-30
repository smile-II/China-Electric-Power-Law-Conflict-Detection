import os
import json

# 定义转换函数，将旧格式转换为新格式
def transform_format(old_data):
    new_data = {
        "publish_date": old_data.get("publish_date"),
        "effective_date": old_data.get("effective_date"),
        "type": old_data.get("office_level"),
        "status": old_data.get("status"),
        "title": old_data.get("title"),
        "office": old_data.get("office"),
        "office_category": old_data.get("office_category"),
        "effective_period": old_data.get("effective_period"),
        "content": old_data.get("content")
    }
    return new_data

# 定义要处理的文件路径
input_file_path = 'data/raw_datasets/laws_zyp/combined_laws.json'
# 输出文件路径
output_file_path = 'data/raw_datasets/laws_zyp/combined_laws_transformed.json'

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        data = json.loads(line.strip())
        # 转换格式
        transformed_data = transform_format(data)
        # 将转换后的数据按行写入输出文件
        output_file.write(json.dumps(transformed_data, ensure_ascii=False) + '\n')

print(f"转换格式后的文件已按行保存到 {output_file_path}")
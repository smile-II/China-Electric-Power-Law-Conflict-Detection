# import json

# def split_legal_content(record):
#     """
#     将长篇法律条例文本拆分为单条条例
#     """
#     content = record["content"]
#     # 以换行符和空格作为分隔符拆分内容
#     items = content.split('\n\n')
#     split_items = []
    
#     for item in items:
#         item = item.strip()
#         if item:
#             split_record = record.copy()
#             split_record["content"] = item
#             split_items.append(split_record)
    
#     return split_items

# def save_split_legal_items(input_file, output_file):
#     """
#     拆分法律文本并保存为单条JSON记录
#     """
#     with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
#         for line in infile:
#             record = json.loads(line.strip())
#             split_items = split_legal_content(record)
#             for item in split_items:
#                 json.dump(item, outfile, ensure_ascii=False)
#                 outfile.write('\n')
#     print(f"拆分后的法律条目已保存为 {output_file}")

# if __name__ == "__main__":
#     input_file = "data/raw_datasets/electricity_laws_content.json"  # 输入文件路径
#     output_file = "data/raw_datasets/split_electricity_laws.json"  # 输出文件路径
#     save_split_legal_items(input_file, output_file)


import json

def split_legal_content(record):
    """
    将长篇法律条例文本拆分为单条条例
    """
    content = record["content"]
    # 使用换行符作为分隔符拆分内容
    items = content.split('\n')
    split_items = []
    
    for item in items:
        item = item.strip()
        if item:
            split_record = record.copy()
            split_record["content"] = item
            split_items.append(split_record)
    
    return split_items

def save_split_legal_items(input_file, output_file):
    """
    拆分法律文本并保存为单条JSON记录
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line.strip())
            split_items = split_legal_content(record)
            for item in split_items:
                json.dump(item, outfile, ensure_ascii=False)
                outfile.write('\n')
    print(f"拆分后的法律条目已保存为 {output_file}")

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws.json"  # 输入文件路径
    output_file = "data/processed/split_electricity_laws.json"  # 输出文件路径
    save_split_legal_items(input_file, output_file)

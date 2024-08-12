import json

# 输入文件名
input1_filename = 'D:\project\legal\data\processed\electricity_laws_20240730_2862_title.json'
input2_filename = 'D:\project\legal\output\conflict_results-1-20240801.json'
# 输出文件名
output_filename = 'D:\project\legal\output\conflict_results-combine-20240801.json'

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return json.load(infile)

# 读取输入文件
input1_data = read_json_file(input1_filename)
input2_data = read_json_file(input2_filename)

# 构建一个字典以便快速查找title信息
title_lookup = {entry['doc_index']: entry['title'] for entry in input1_data}

# 处理第二个文件的数据，添加title信息
for entry in input2_data:
    doc_index = entry['doc_index']
    if doc_index in title_lookup:
        entry['conflict']['input_title'] = title_lookup[doc_index]

# 将处理后的数据写入输出文件
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(input2_data, outfile, ensure_ascii=False, indent=4)

print(f'处理完成，结果已保存到 {output_filename}')
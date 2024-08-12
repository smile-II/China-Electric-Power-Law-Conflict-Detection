import json

# 输入文件名
input_filename = 'D:\project\legal\data\processed\electricity_laws_20240730_2862.json'
# 输出文件名
output_filename = 'D:\project\legal\data\processed\electricity_laws_20240730_2862_title.json'

# 读取输入文件
with open(input_filename, 'r', encoding='utf-8') as infile:
    # 逐行读取输入文件内容
    input_lines = infile.readlines()

# 处理后的数据列表
processed_data = []

# 遍历输入的每一行
for index, line in enumerate(input_lines):
    # 解析每行JSON数据
    data = json.loads(line.strip())
    # 提取需要的字段
    processed_entry = {
        "doc_index": index,
        "title": data.get("title", "")
    }
    # 将处理后的数据添加到列表中
    processed_data.append(processed_entry)

# 将处理后的数据写入输出文件
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(processed_data, outfile, ensure_ascii=False, indent=4)

print(f'处理完成，结果已保存到 {output_filename}')

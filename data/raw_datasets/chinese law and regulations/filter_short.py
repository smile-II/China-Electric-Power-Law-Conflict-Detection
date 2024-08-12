import json

def is_content_too_short(record, min_length):
    """
    判断content内容是否过短
    """
    return len(record['content']) < min_length

def filter_and_split_legal_items(input_file, output_file, min_length):

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line.strip())
            if not is_content_too_short(record, min_length):
                    json.dump(record, outfile, ensure_ascii=False)
                    outfile.write('\n')
    print(f"过滤和拆分后的法律条目已保存为 {output_file}")

if __name__ == "__main__":
    input_file = r"D:\project\legal\data\raw_datasets\chinese law and regulations\filtered_laws_with_content_split_20240812.json"   # 输入文件路径
    output_file = r"D:\project\legal\data\raw_datasets\chinese law and regulations\filtered_laws_with_content_split_20240812_short.json"   # 输出文件路径
    filter_and_split_legal_items(input_file, output_file, min_length = 25)

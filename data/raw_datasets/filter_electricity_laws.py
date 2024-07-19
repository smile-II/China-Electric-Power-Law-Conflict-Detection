import json

def is_electricity_related(title):
    """
    判断标题是否与电力相关
    """
    keywords = ["电力", "电网", "电气", "电能"]
    return any(keyword in title for keyword in keywords)

def filter_electricity_laws(input_file, output_file):
    """
    过滤与电力相关的法律文件，并保存为新文件
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line.strip())
            if is_electricity_related(record['title']):
                json.dump(record, outfile, ensure_ascii=False)
                outfile.write('\n')
    print(f"与电力相关的法律文件已保存为 {output_file}")

import json

def is_electricity_related(title):
    """
    判断标题是否与电力相关
    """
    keywords = ["电力", "电网", "电气", "电能"]
    return any(keyword in title for keyword in keywords)

def filter_electricity_laws(input_file, output_file):
    """
    过滤与电力相关的法律文件，并保存为新文件，同时输出这些法律的标题
    """
    electricity_laws = []
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line.strip())
            if is_electricity_related(record['title']):
                electricity_laws.append(record)
                json.dump(record, outfile, ensure_ascii=False)
                outfile.write('\n')
    
    print(f"与电力相关的法律文件已保存为 {output_file}")
    print("\n以下是过滤得到的电力相关法律文件的标题：")
    for law in electricity_laws:
        print(law['title'])


if __name__ == "__main__":
    input_file = "data/raw_datasets/default.json"
    output_file = "data/raw_datasets/electricity_laws_content.json"
    filter_electricity_laws(input_file, output_file)

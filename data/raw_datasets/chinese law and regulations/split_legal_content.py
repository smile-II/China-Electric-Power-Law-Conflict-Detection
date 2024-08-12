import json
import re

def split_legal_content(record):
    """
    将长篇法律条例文本拆分为单条条例
    """
    content = record["content"]
    
    # 按“第XX条”分割文本
    split_text = re.split(r'(第[\d一二三四五六七八九十]+条(?:\s|\n))', content)

    # 组合条款，使每个条款包含“第XX条”开头及其内容
    articles = []
    for i in range(1, len(split_text), 2):
        # 获取“第XX条”开头及其内容
        article = split_text[i] + split_text[i + 1]
        # 找到最后一个句号的位置
        last_period_index = article.rfind('。')
        # 如果找到句号，则去除句号之后的内容
        if last_period_index != -1:
            article = article[:last_period_index + 1]
        articles.append(article)
        
    # 去除第一条之前的所有内容
    start_index = 0
    for i, article in enumerate(articles):
        if '第一条' in article:
            start_index = i
            break

    # 保留从第一条开始的所有条款
    split_items = []
    for article in articles[start_index:]:
        split_record = record.copy()
        split_record["content"] = article
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
    input_file = r"D:\project\legal\data\raw_datasets\chinese law and regulations\Shanghai_Electric_Power_Company_Internal_Policy_Document.json"  # 输入文件路径
    output_file = r"D:\project\legal\data\raw_datasets\chinese law and regulations\Shanghai_Electric_Power_Company_Internal_Policy_Document_split_20240812.json"  # 输出文件路径
    save_split_legal_items(input_file, output_file)

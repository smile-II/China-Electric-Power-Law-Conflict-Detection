import re

def split_into_sentences(paragraph):
    # 使用正则表达式将段落分割成句子，包括中文的句号、问号、感叹号
    sentences = re.split(r'(?<=[。！？])\s*', paragraph)
    return [s for s in sentences if s]  # 移除空句子

# 示例使用
paragraph = "这是第一句话。这里是第二句话！这是第三句话？"
sentences = split_into_sentences(paragraph)
for i, sentence in enumerate(sentences):
    print(f"句子 {i+1}: {sentence}")

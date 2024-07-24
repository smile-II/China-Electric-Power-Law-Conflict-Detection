import json
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from retriever import retrieve
from sentence_transformers import SentenceTransformer

# 加载模型
print("加载模型中...")
re_model = SentenceTransformer('moka-ai/m3e-base')
model_name = 'IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
print("模型加载完成")


# 定义标签，仅包括“法律文本冲突”和“法律文本不冲突”
label_map = {0: '法律文本冲突', 1: '法律文本不冲突', 2: '法律文本不冲突'}

def predict_conflict(text1, text2):
    inputs = tokenizer.encode_plus(text1, text2, return_tensors='pt', truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    return label_map[predicted_label]

def detect_conflicts(input_law, retrieved_laws):
    results = []
    for index, law in enumerate(retrieved_laws):
        if isinstance(law, dict) and 'content' in law:
            label = predict_conflict(input_law, law['content'])
            result = {
                "input_index": index,
                "input_text": input_law,
                "retrieved_index": index,
                "retrieved_text": law['content'],
                "label": label
            }
            results.append(result)
    return results

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws_20240722_7262.json"
    
    # 加载输入的法律文档
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]
    
    # 假设我们有一个输入的法律文档
    input_law = "电力供应、使用双方根据平等自愿、协商一致的原则签订供用电合同。"  # 这里使用示例文档内容

    # 开始计时
    start_time = time.time()

    # 检索相似的法律文档
    retrieved_laws, vectorize_time, similarity_time, sort_time = retrieve(input_law, re_model, "models/vectorizer.pkl", input_file)
    end_retrieved_time = time.time()

    # 检测冲突
    conflicts = detect_conflicts(input_law, retrieved_laws)
    end_conflicts_time = time.time()

    # 输出结果
    for conflict in conflicts:
        print(f"索引: {conflict['retrieved_index']} - 标签: {conflict['label']}")
        print(f"输入文本: {conflict['input_text']}")
        print(f"检索文本: {conflict['retrieved_text']}/n")

    # 输出时间
    print(f"检索时间: {end_retrieved_time - start_time} 秒")
    print(f"冲突检测时间: {end_conflicts_time - end_retrieved_time} 秒")
    print(f"总时间: {end_conflicts_time - start_time} 秒")

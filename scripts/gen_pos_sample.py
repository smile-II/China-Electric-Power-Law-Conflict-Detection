import json
import random
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from sentence_transformers import SentenceTransformer
from retriever import retrieve
from openai import OpenAI

client = OpenAI(api_key="your key", base_url="https://api.deepseek.com")

def chat_with_model(input_text, temperature=1.25):
    # 调用OpenAI API的chat接口
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个友好的助手。"},
            {"role": "user", "content": input_text}
        ],
        stream=False,
        temperature=temperature,
    )
    return response.choices[0].message.content
# 使用LLM进行改写
generator = pipeline("text-generation", model="gpt-3.5-turbo")  # 替换为你选择的LLM模型

def predict_conflict(text1, text2):
    inputs = tokenizer.encode_plus(text1, text2, return_tensors='pt', truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    return label_map[predicted_label]

def generate_negative_sample(positive_sample):
    # 使用LLM改写生成负样本
    response = generator(f"将以下内容改写成与原文冲突的法律条文：{positive_sample}", max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

def generate_dataset(input_file, output_file, model, top_k=5):
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    dataset = []

    for doc in documents:
        input_text = doc['content']

        # 检索相似文本
        retrieved_laws, _, _, _ = retrieve(input_text, re_model, "models/vectorizer.pkl", input_file, top_k=top_k)

        if retrieved_laws:
            # 随机选择一个检索结果作为正样本
            positive_sample = random.choice(retrieved_laws)['content']
            dataset.append({
                "input_text": input_text,
                "retrieved_text": positive_sample,
                "label": 1
            })

            # 使用LLM生成负样本
            negative_sample = generate_negative_sample(positive_sample)
            dataset.append({
                "input_text": input_text,
                "retrieved_text": negative_sample,
                "label": 0
            })

    # 保存数据集
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 加载模型
    re_model = SentenceTransformer('moka-ai/m3e-base')
    input_file = "data/processed/electricity_laws.json"
    output_file = "data/processed/generated_dataset.json"
    generate_dataset(input_file, output_file, re_model)

import json
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from retriever import retrieve
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re
# 加载模型
print("加载模型中...")
re_model = SentenceTransformer('moka-ai/m3e-base')
model_name = 'IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print("模型加载完成")

# 定义标签，仅包括“法律文本冲突”和“法律文本不冲突”
label_map = {0: '法律文本冲突', 1: '法律文本不冲突', 2: '法律文本不冲突'}

def predict_conflict(text1, text2):
    inputs = tokenizer.encode_plus(text1, text2, return_tensors='pt', truncation=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    return label_map[predicted_label]

def detect_conflicts(input_law, retrieved_laws):
    results = []
    for index, law in enumerate(retrieved_laws):
        if isinstance(law, dict) and 'content' in law:
            # 预处理，删除前面的第XX条之类的内容
            preprocessed_input_law = re.sub(r'^第[一二三四五六七八九十百千万\d]+条\s*', '', input_law)
            preprocessed_retrieved_text = re.sub(r'^第[一二三四五六七八九十百千万\d]+条\s*', '', law['content'])
            label = predict_conflict(preprocessed_input_law, preprocessed_retrieved_text)
            result = {
                "input_text": input_law,
                "retrieved_index": index,
                "retrieved_text": law['content'],
                "label": label
            }
            results.append(result)
    return results

def process_single_document(doc_index, document, input_file, conflict_output_file, retrieval_output_file):
    input_law = document['content']
    
    start_time = time.time()
    
    # 检索相似的法律文档
    retrieved_laws, vectorize_time, similarity_time, sort_time = retrieve(input_law, re_model, "models/vectorizer.pkl", input_file, top_k=10)
    end_retrieved_time = time.time()
    
    # 检测冲突
    conflict_results = detect_conflicts(input_law, retrieved_laws)
    end_conflicts_time = time.time()

    conflicts = []
    retrievals = []

    # 保存冲突结果
    for conflict in conflict_results:
        if conflict['label'] == '法律文本冲突':
            conflicts.append({
                "doc_index": doc_index,
                "conflict": conflict
            })
    
    # 保存检索结果
    retrievals.append({
        "doc_index": doc_index,
        "retrieved_laws": [
            {
                "index": i,
                "publish_date": law.get("publish_date", ""),
                "effective_date": law.get("effective_date", ""),
                "type": law.get("type", ""),
                "status": law.get("status", ""),
                "title": law.get("title", ""),
                "office": law.get("office", ""),
                "office_category": law.get("office_category", ""),
                "effective_period": law.get("effective_period", ""),
                "content": law.get("content", "").replace("\n", " ")  # 删除可能存在的换行符
            }
            for i, law in enumerate(retrieved_laws)
        ],
        "retrieval_time": end_retrieved_time - start_time,
        "conflict_detection_time": end_conflicts_time - end_retrieved_time,
        "total_time": end_conflicts_time - start_time
    })

    with open(conflict_output_file, 'a', encoding='utf-8') as f:
        for conflict in conflicts:
            f.write(json.dumps(conflict, ensure_ascii=False) + '\n')
    
    with open(retrieval_output_file, 'a', encoding='utf-8') as f:
        for retrieval in retrievals:
            f.write(json.dumps(retrieval, ensure_ascii=False) + '\n')

def process_documents(input_file, conflict_output_file, retrieval_output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    # 清空文件内容
    open(conflict_output_file, 'w').close()
    open(retrieval_output_file, 'w').close()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for doc_index, document in enumerate(documents):
            futures.append(executor.submit(process_single_document, doc_index, document, input_file, conflict_output_file, retrieval_output_file))
        
        for future in tqdm(as_completed(futures), total=len(futures)):
            future.result()

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws_20240722_7262.json"
    conflict_output_file = "output/conflict_results.json"
    retrieval_output_file = "output/retrieval_results.json"

    process_documents(input_file, conflict_output_file, retrieval_output_file)
    print(f"冲突检测结果已保存到 {conflict_output_file}")
    print(f"检索结果已保存到 {retrieval_output_file}")

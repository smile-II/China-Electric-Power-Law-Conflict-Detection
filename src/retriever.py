import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
from sentence_transformers import SentenceTransformer

def vectorize_query(query, model):
    start_time = time.time()
    query_embedding = model.encode([query])[0]
    vectorize_time = time.time() - start_time
    return query_embedding, vectorize_time

def calculate_similarities(embeddings, query_embedding):
    start_time = time.time()
    similarities = np.dot(embeddings, query_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding))
    similarity_time = time.time() - start_time
    return similarities, similarity_time

def sort_results(similarities, documents, top_k):
    start_time = time.time()
    top_k_indices = similarities.argsort()[-top_k:][::-1]
    
    # 将相似度转换为 Python 的 float 类型
    top_k_documents = [
        {**documents[idx], "similarity": float(similarities[idx])} 
        for idx in top_k_indices
    ]
    
    sort_time = time.time() - start_time
    return top_k_documents, sort_time

def retrieve(query, model, model_file, data_file, top_k=20):
    # 加载索引模型
    with open(model_file, 'rb') as f:
        embeddings, documents = pickle.load(f)

    # 使用线程池进行并行化处理
    with ThreadPoolExecutor() as executor:
        future_query_embedding = executor.submit(vectorize_query, query, model)
        query_embedding, vectorize_time = future_query_embedding.result()

        future_similarities = executor.submit(calculate_similarities, embeddings, query_embedding)
        similarities, similarity_time = future_similarities.result()

        future_results = executor.submit(sort_results, similarities, documents, top_k)
        top_k_documents, sort_time = future_results.result()

    return top_k_documents, vectorize_time, similarity_time, sort_time

if __name__ == "__main__":
    
    query = "第三十一条  企业在来料加工、贴牌生产、委托加工时，企业知识产权管理部门应协助相关部门收集对方的相关知识产权信息，必要时应要求其提供相应的知识产权权属证明。\n\n企业应在合同中明确约定相应的知识产权权属、知识产权的许可使用范围、侵犯第三人知识产权时的责任承担等内容。"  # 示例查询
    re_model = SentenceTransformer('moka-ai/m3e-base')
    model_file = "models/Shanghai_Enterprise_Compliance_Analysis_Upper_Level_Legal_Database_20240812"
    data_file = "data\processed\electricity_laws_20240730_2970.json"
    results, vectorize_time, similarity_time, sort_time = retrieve(query, re_model, model_file, data_file)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Content: {result['content']}")
        print(f"Similarity: {result['similarity']}\n")

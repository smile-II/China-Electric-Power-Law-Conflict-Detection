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
    top_k_documents = [documents[idx] for idx in top_k_indices]
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
    
    query = "电力供应、使用双方根据平等自愿、协商一致的原则签订供用电合同。"  # 示例查询
    re_model = SentenceTransformer('moka-ai/m3e-base')
    model_file = "models/vectorizer.pkl"
    data_file = "data\processed\electricity_laws_20240722_7262.json"
    results, vectorize_time, similarity_time, sort_time = retrieve(query, re_model, model_file, data_file)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Content: {result['content']}\n")

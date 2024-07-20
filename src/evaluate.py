from sentence_transformers import SentenceTransformer
import json
import time
import numpy as np
from retriever import retrieve
from sklearn.metrics.pairwise import cosine_similarity

def evaluate(input_file, model_file, model):
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    queries = ["电力法", "电力设施保护", "供电合同"]  # 电力法律相关的查询示例

    for query in queries:
        start_time = time.time()
        results, vectorize_time, similarity_time, sort_time = retrieve(query, model, model_file, input_file)
        end_time = time.time()

        # 计算查询与检索到的每个文档的余弦相似度
        query_vector = model.encode([query])[0]
        document_vectors = [model.encode([doc['content']])[0] for doc in results]
        cosine_similarities = cosine_similarity([query_vector], document_vectors).flatten()

        # 计算平均余弦相似度
        average_cosine_similarity = np.mean(cosine_similarities) if cosine_similarities.size > 0 else 0

        print(f"Query: {query}")
        print(f"Average Cosine Similarity: {average_cosine_similarity}")
        print(f"Vectorize Time: {vectorize_time} seconds")
        print(f"Similarity Calculation Time: {similarity_time} seconds")
        print(f"Sorting Time: {sort_time} seconds")
        print(f"Total Time Taken: {end_time - start_time} seconds")
        print()

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws.json"
    model_file = "models/vectorizer_minilm.pkl"
    
    # 提前加载模型
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    evaluate(input_file, model_file, model)

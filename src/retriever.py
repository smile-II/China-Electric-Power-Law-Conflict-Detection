import json
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def retrieve(query, model_file, data_file):
    with open(model_file, 'rb') as f:
        vectorizer, X = pickle.load(f)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]
    
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, X).flatten()
    top_indices = similarities.argsort()[-5:][::-1]  # 返回前5个最相似的文档索引
    
    results = [documents[i] for i in top_indices]
    return results

if __name__ == "__main__":
    query = "电力供应、使用双方根据平等自愿、协商一致的原则签订供用电合同，确定双方的权利和义务，明确约定产权分界、供用电设施维护责任的划分、违约责任等。"  # 示例查询
    model_file = "models/vectorizer.pkl"
    data_file = "data/processed/electricity_laws.json"
    results = retrieve(query, model_file, data_file)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Content: {result['content']}\n")

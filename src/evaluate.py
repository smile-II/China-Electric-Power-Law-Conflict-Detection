import json
import time
from retriever import retrieve

def evaluate(input_file, model_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    queries = ["电力供应", "电网管理", "电价"]  # 示例查询
    for query in queries:
        start_time = time.time()
        results = retrieve(query, model_file, input_file)
        end_time = time.time()

        # 查找与查询相关的文档
        relevant_docs = [doc for doc in documents if query in doc['content']]
        
        # 检查检索结果中有多少是相关的
        retrieved_relevant = [res for res in results if any(query in doc['content'] for doc in relevant_docs)]
        
        # 计算评价指标
        precision = len(retrieved_relevant) / len(results) if results else 0
        recall = len(retrieved_relevant) / len(relevant_docs) if relevant_docs else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

        print(f"Query: {query}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")
        print(f"Time Taken: {end_time - start_time} seconds")
        print()




if __name__ == "__main__":
    input_file = "data/processed/electricity_laws.json"
    model_file = "models/vectorizer.pkl"
    evaluate(input_file, model_file)

import json
import pickle
from sentence_transformers import SentenceTransformer

def build_index(input_file, output_model):
    # 加载 all-MiniLM-L6-v2 模型
    model = SentenceTransformer('moka-ai/m3e-base')
    
    # 读取文档内容
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    # 提取内容并使用模型进行向量化
    contents = [doc['content'] for doc in documents]
    embeddings = model.encode(contents, show_progress_bar=True)

    # 保存向量化结果和完整文档
    with open(output_model, 'wb') as f:
        pickle.dump((embeddings, documents), f)

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws.json"
    output_model = "models/vectorizer.pkl"
    build_index(input_file, output_model)

from flask import Flask, request, jsonify, render_template
from retriever import retrieve
from sentence_transformers import SentenceTransformer
from sentence_splitter import split_into_sentences

app = Flask(__name__)

# 提前加载模型
model = SentenceTransformer('moka-ai/m3e-base')
model_pkl = "models/Shanghai_Enterprise_Compliance_Analysis_Upper_Level_Legal_Database_20240812"
input_file = "data/processed/Shanghai_Enterprise_Compliance_Analysis_Upper_Level_Legal_Database_20240812.json"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST']) #定义一个POST请求的路由，处理搜索请求。
def search():
    query = request.json.get('query')
    query_list = split_into_sentences(query)
    
    results_list = []
    for query in query_list:
        results, vectorize_time, similarity_time, sort_time = retrieve(query, model, model_pkl, input_file ,top_k=15)
        
        # 为每个检索结果添加相似度信息
        processed_results = []
        for result in results:
            processed_results.append(result)
        
        results_list.append({
            "query": query,
            "results": processed_results,
            "vectorize_time": vectorize_time,
            "similarity_time": similarity_time,
            "sort_time": sort_time
        })
    
    return jsonify(results_list)


if __name__ == "__main__":
    app.run(debug=True)

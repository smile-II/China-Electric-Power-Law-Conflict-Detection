from flask import Flask, request, jsonify, render_template
from retriever import retrieve
from sentence_transformers import SentenceTransformer
from sentence_splitter import split_into_sentences

app = Flask(__name__)

# 提前加载模型
model = SentenceTransformer('moka-ai/m3e-base')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    query_list = split_into_sentences(query)
    
    results_list = []
    for query in query_list:
        results, vectorize_time, similarity_time, sort_time = retrieve(query, model, "models/vectorizer.pkl", "data/processed/electricity_laws.json")
        results_list.append({
            "query": query,
            "results": results,
            "vectorize_time": vectorize_time,
            "similarity_time": similarity_time,
            "sort_time": sort_time
        })
    
    return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)

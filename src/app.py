from flask import Flask, request, jsonify
from retriever import retrieve

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    results = retrieve(query, "models/vectorizer.pkl", "data/raw_datasets/split_electricity_laws.json")
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

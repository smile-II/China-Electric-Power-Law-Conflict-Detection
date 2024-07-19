from flask import Flask, request, jsonify, render_template
from retriever import retrieve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    results = retrieve(query, "models/vectorizer.pkl", "data/processed/electricity_laws.json")
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def build_index(input_file, output_model):
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = [json.loads(line)['content'] for line in f]
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    
    with open(output_model, 'wb') as f:
        pickle.dump((vectorizer, X), f)

if __name__ == "__main__":
    input_file = "data/processed/electricity_laws.json"
    output_model = "models/vectorizer.pkl"

        
    build_index(input_file, output_model)

from collections import defaultdict
import re

# Sample documents
documents = {
1: "The quick brown fox jumps over the lazy dog.",
2: "A brown fox is fast and dog is lazy.",
3: "The sun is shining, and the weather is warm."
}

# Fubction to tokenize and preprocess a document
def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\w+',text)
    return set(tokens)
    
# Initialize the inverted index    
inverted_index = defaultdict(set)

# Create the inverted index
for doc_id, doc_text in documents.items():
    terms = preprocess(doc_text)
    for term in terms:
        inverted_index[term].add(doc_id)
        
# Query function
def query(query_text):
    terms = preprocess(query_text)
    results = set(doc_id for term in terms for doc_id in inverted_index.get(term,[]))
    return results

# Example query    
query_result = query("brown fox")
print("Documents containing 'brown' and 'fox' :", query_result)

query_result = query("sun shining")
print("Documents containing 'sun' and 'shining' :", query_result)
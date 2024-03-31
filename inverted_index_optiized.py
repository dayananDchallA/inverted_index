import re
from collections import defaultdict
from multiprocessing import Pool

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)  # Using defaultdict to store posting lists

    def preprocess_text(self, text):
        # Tokenization and normalization
        terms = re.findall(r'\b\w+\b', text.lower())
        return set(terms)  # Remove duplicates

    def add_document(self, doc_id, text):
        terms = self.preprocess_text(text)
        for term in terms:
            self.index[term].append(doc_id)

    def _process_chunk(self, chunk):
        doc_id, text = chunk
        self.add_document(doc_id, text)

    def index_documents_parallel(self, documents, num_processes=4):
        with Pool(num_processes) as pool:
            pool.map(self._process_chunk, documents.items())

    def search(self, query):
        query_terms = self.preprocess_text(query)
        result_docs = None
        for term in query_terms:
            if result_docs is None:
                result_docs = set(self.index.get(term, []))
            else:
                result_docs = result_docs.intersection(set(self.index.get(term, [])))
        return list(result_docs) if result_docs is not None else []

# Example usage
if __name__ == "__main__":
    index = InvertedIndex()

    # Populate index with documents
    documents = {
        1: "This is a sample document",
        2: "Another document for testing purposes",
        # Add more documents here...
    }

    # Index documents in parallel
    index.index_documents_parallel(documents)

    # Search example
    query = "sample testing"
    results = index.search(query)
    print("Search results for query '{}':".format(query))
    for doc_id in results:
        print("- Document ID:", doc_id)

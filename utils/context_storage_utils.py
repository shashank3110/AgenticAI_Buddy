"""
Storage Utils:
Fore vector index based storage for context retrieval.
"""
import os
import faiss
import numpy as np
from openai import OpenAI
import json

def get_vector_index(index_path):
    """
    Check if vector index file exists else create one.
    """
    dimension = 1536 # text embedding model's dimension
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)   
    
    else: # create an index file using random vectors
        nlist = 100  # Number of clusters for the IVF index
        quantizer = faiss.IndexFlatL2(dimension)  # Use flat quantizer to get base vectors
        index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)
        random_vectors = np.random.random((4000, dimension)).astype('float32')
        index.train(random_vectors)
        faiss.write_index(index, index_path)

    return index


def write_to_knowledge_base(query_response, index_path='metadata/faiss_index.faiss'):
    """
    Update knowldege base and return index.
    """
    vectors = get_query_vector(query_response)
    index = faiss.read_index(index_path)
    index.add(vectors)
    faiss.write_index(index, index_path)

    return index

def get_query_vector(input_text):
    """
    Generate embeddings vector for given text input.
    """
    client = OpenAI() 
    embeddings =  client.embeddings.create(
                        input=input_text, model="text-embedding-3-small"
                    ).data[0].embedding #["data"][0]["embedding"]
    
    vectors = np.array(embeddings).astype("float32").reshape(1, -1)

    return vectors

def setup_data(path = 'metadata/context_history.jsonl'):
    """
    Create  json file to store raw data for knowledge base. 
    """
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass

def write_data(history, metadata_path):
    """
    Write query history docs
    """

    with open(metadata_path, "a") as f:
        f.write(json.dumps(history) + "\n")

def load_data(filepath="metadata/context_history.jsonl"):
    """
    Load raw data for context retrieval
    """
    history = []
    with open(filepath, "r") as f:
        for line in f:
            history.append(json.loads(line))
    return history    


def get_context(distances, indices, threshold=0.1):
    """
    Return raw data for most relevant context.
    """
    history = load_data()
    context = []
    print(f'search indices: {indices[0]} \n search distances:{distances[0]}')

    for dist, idx in zip(distances[0], indices[0]):
        if dist <= threshold:
            context.append(history[idx]['response'])

    print(f'Retrieved context:{context}')
    return context



import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Sample data
data = {
    "Client_ID": [101, 102, 103],
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [29, 34, 42],
    "Pickup_Date": ["2023-01-15", "2023-02-15", "2023-03-15"],
    "Hamper_Type": ["Standard", "Premium", "Standard"],
    "Location": ["Downtown", "Uptown", "Midtown"]
}

transaction_data = pd.DataFrame(data)
transaction_narrative = "Here are the latest client transactions:\n"
for _, row in transaction_data.iterrows():
    transaction_narrative += (
        f"Client {row['Client_ID']} ({row['Name']}, Age {row['Age']}) picked "
        f"up a {row['Hamper_Type']} hamper at {row['Location']} on {row['Pickup_Date']}.\n"
    )

documents = {
    "doc1": (
        "XYZ Charity is a non-profit organization focused on distributing food hampers. "
        "It aims to improve community well-being by providing support to families in need."
    ),
    "doc2": transaction_narrative
}

# Load pipelines
embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Embed documents
doc_embeddings = {
    doc_id: torch.tensor(embedder(text)).mean(dim=1)
    for doc_id, text in documents.items()
}

def retrieve_context(query, top_k=2):
    query_emb = torch.tensor(embedder(query)).mean(dim=1)
    scores = {
        doc_id: cosine_similarity(query_emb, emb).item()
        for doc_id, emb in doc_embeddings.items()
    }
    top_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
    return "\n\n".join(documents[doc_id] for doc_id in top_ids)

def query_llm(query, context):
    """
    Constructs a prompt with improved instructions for better answers.
    """
    prompt = (
        "You are a helpful assistant. The user is asking questions based on transaction and charity data.\n"
        "Analyze everything and provide a complete and accurate answer based on all relevant information.\n"
        "List all relevant matches if the question asks for locations, people, or summaries.\n\n"
        f"Context:\n{context}\n\n"
        f"User Query: {query}\n\n"
        "Answer:"
    )

    outputs = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    raw_output = outputs[0]['generated_text']

    # Remove repeated prompt if generated
    if raw_output.startswith(prompt):
        raw_output = raw_output[len(prompt):].strip()

    return raw_output.strip()


def rag_chatbot(query):
    context = retrieve_context(query)
    return query_llm(query, context)

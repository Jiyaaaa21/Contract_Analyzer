import os
import re
import numpy as np
from dotenv import load_dotenv
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

bi_encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def embed_chunks(chunks):
    return bi_encoder.encode(chunks, convert_to_tensor=True)

def retrieve_chunks(question, chunks, embeddings, top_k=3):
    q_emb = bi_encoder.encode([question], convert_to_tensor=True)
    scores = cosine_similarity(q_emb.cpu().numpy(), embeddings.cpu().numpy())[0]
    idxs = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in idxs]

def summarize_text(text):
    if len(text.split()) > 1024:
        text = " ".join(text.split()[:1024])
    return summarizer(text, max_length=200, min_length=50, do_sample=False)[0]['summary_text']

def answer_question(chunks, embeddings, question, text):
    relevant = retrieve_chunks(question, chunks, embeddings)
    context = "\n\n".join(relevant)
    messages = [
        {"role": "system", "content": "You are a legal assistant that answers questions based on contracts."},
        {"role": "user", "content": f"Contract:\n{text}\n\nQuestion: {question}"}
    ]
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.2)
    return response.choices[0].message.content.strip()

def extract_start_end_dates(text):
    messages = [
        {"role": "system", "content": "You extract date ranges from legal contracts."},
        {"role": "user", "content": f"When does the agreement start and end?\n\n{text}"}
    ]
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.2)
    return response.choices[0].message.content.strip()

def check_contract_renewal(text):
    messages = [
        {"role": "system", "content": "You determine if a contract has a renewal clause."},
        {"role": "user", "content": f"Is there a renewal or extension clause in this contract?\n\n{text}"}
    ]
    response = openai.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.2)
    return response.choices[0].message.content.strip()


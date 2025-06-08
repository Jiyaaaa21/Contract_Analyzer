from transformers import pipeline

# You can use 'deepset/roberta-base-squad2' or 'bert-base-uncased' or 'nlpaueb/legal-bert-base-uncased'
def get_qa_pipeline():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")

def get_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
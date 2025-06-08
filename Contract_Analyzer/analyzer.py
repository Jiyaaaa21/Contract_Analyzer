def analyze_contract(text, question, qa_pipeline):
    return qa_pipeline(question=question, context=text)

def summarize_contract(text, summarizer):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""
    for chunk in chunks:
        res = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summary += res[0]['summary_text'] + "\n"
    return summary.strip()
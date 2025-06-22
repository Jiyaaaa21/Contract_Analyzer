from utils.pdf_utils import extract_text_from_pdf
from utils.NLP_utils import chunk_text, embed_chunks, summarize_text, answer_question, extract_start_end_dates, check_contract_renewal

class ContractAnalyzer:
    def __init__(self, pdf_path):
        self.text = extract_text_from_pdf(pdf_path)
        self.chunks = chunk_text(self.text)
        self.embeds = embed_chunks(self.chunks)

    def summarize(self):
        return summarize_text(self.text)

    def ask(self, question):
        ql = question.lower()
        if any(kw in ql for kw in ["start and end date", "agreement duration", "begin and end", "end date"]):
            return extract_start_end_dates(self.text)
        if any(kw in ql for kw in ["renew", "extension", "renewal", "extend"]):
            return check_contract_renewal(self.text)
        return answer_question(self.chunks, self.embeds, question, self.text)
    
    
    

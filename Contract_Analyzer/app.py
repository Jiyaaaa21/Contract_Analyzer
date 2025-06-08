import streamlit as st
import os
st.write("📁 Current directory:", os.getcwd())
st.write("📄 Does file exist:", os.path.exists("sample_contract.txt"))
from model_utils import get_qa_pipeline, get_summarizer
from analyzer import analyze_contract, summarize_contract

# Load models
qa_pipeline = get_qa_pipeline()
summarizer = get_summarizer()

st.title("🤖 Contract Analyzer with Hugging Face")

# Load contract
try:
    with open("sample_contract.txt", "r", encoding="utf-8") as f:
        contract_text = f.read()
    st.write(f"✅ Loaded contract: {len(contract_text)} characters")
except Exception as e:
    st.error(f"❌ Error reading file: {e}")
    contract_text = ""


# Display contract preview
with st.expander("📄 View Contract Text"):
        if contract_text:
            st.text_area("Contract Text Preview", contract_text, height=300)
        else:
            st.warning("Contract text is empty or could not be loaded.")


# Option to ask questions
st.subheader("🔍 Ask a Question about the Contract")
user_question = st.text_input("Enter your question:")

if st.button("Get Answer") and user_question:
    answer = analyze_contract(contract_text, user_question, qa_pipeline)
    st.success(f"**Answer:** {answer['answer']}")

# Option to summarize
if st.button("Summarize Contract"):
    st.subheader("📝 Summary")
    summary = summarize_contract(contract_text, summarizer)
    st.write(summary[0]['summary_text'] if summary else "No summary generated.")
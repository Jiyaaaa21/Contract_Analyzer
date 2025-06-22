import streamlit as st
import tempfile
from main import ContractAnalyzer

st.set_page_config(page_title="📄 AI Contract Analyzer", layout="centered")

st.markdown("""
<style>
.main-title { font-size: 2.5rem; font-weight: bold; color: #2E86C1; text-align: center; }
.subtitle  { font-size: 1.1rem; color: #5D6D7E; text-align: center; margin-bottom: 2rem; }
.stButton>button { background-color: #2E86C1; color: white; padding: .6em 1.2em; border-radius: 8px; }
.stTextInput>div>input { border-radius: 8px; padding: .4em .8em; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📜 AI Contract Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your contract PDF, get a summary, and ask legal questions.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
question = st.text_input("Ask a question about the contract")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    analyzer = ContractAnalyzer(path)

    with st.expander("Summary", expanded=True):
        st.write(analyzer.summarize())

    if question:
        with st.spinner("Analyzing..."):
            answer = analyzer.ask(question)
        st.subheader("Answer")
        st.write(answer)

        




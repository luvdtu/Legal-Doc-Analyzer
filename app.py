import streamlit as st
import openai
import os
import fitz  # PyMuPDF for PDF text extraction
from dotenv import load_dotenv
from database import save_document, fetch_all_documents, search_documents_by_keyword
import re

load_dotenv()

# Set Together.ai API config
openai.api_key = os.getenv("TOGETHER_API_KEY")
openai.api_base = "https://api.together.xyz/v1"

# AI analysis function
def analyze_legal_text(text):
    response = openai.ChatCompletion.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": "You are a legal document analysis expert."},
            {"role": "user", "content": f"Analyze this legal document:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# Clause extraction function
def extract_clauses(text):
    # Splitting text into clauses based on common legal headings
    clauses = re.split(r'\n(?=(Clause|Section|Article)\s+\d+[:.]?)', text, flags=re.IGNORECASE)
    clause_list = []
    for i in range(1, len(clauses), 2):
        heading = clauses[i].strip()
        content = clauses[i + 1].strip()
        clause_list.append((heading, content))
    return clause_list

# Chat with document function
def chat_with_document(document_text, user_question):
    response = openai.ChatCompletion.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": "You are a legal document assistant."},
            {"role": "user", "content": f"Based on the following document, {user_question}\n\nDocument:\n{document_text}"}
        ],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# Streamlit UI starts here
st.set_page_config(page_title="Legal Document Analyzer", layout="wide")
st.title("⚖️ AI-Powered Legal Document Analyzer")
st.markdown("⚠️ Struggling to comprehend complex legal documents? Let AI break them down clause-by-clause and answer your questions — all with one click.")

tabs = st.tabs(["📄 Analyze Document", "📊 View All", "🔍 Search", "💬 Chat with Document"])

# 1. Analyze Tab
with tabs[0]:
    st.header("📄 Paste or Upload Legal Document")

    option = st.radio("Input method:", ["Paste Text", "Upload File"])

    document_text = ""

    if option == "Paste Text":
        document_text = st.text_area("Enter document text here", height=250)

    else:
        uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                document_text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
                    text_chunks = [page.get_text() for page in pdf]
                    document_text = "\n".join(text_chunks)

    if document_text and st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing document with Together.ai..."):
            clauses = extract_clauses(document_text)
            analysis_results = []
            for heading, content in clauses:
                analysis = analyze_legal_text(content)
                analysis_results.append((heading, content, analysis))
            save_document(document_text, str(analysis_results))
        st.success("✅ Analysis complete and saved!")
        st.subheader("📊 Clause-wise Analysis")
        for heading, content, analysis in analysis_results:
            with st.expander(f"{heading}"):
                st.markdown("**Clause Content:**")
                st.write(content)
                st.markdown("**AI Analysis:**")
                st.write(analysis)

# 2. View All Tab
with tabs[1]:
    st.header("📜 All Analyzed Documents")
    records = fetch_all_documents()
    for r in records:
        with st.expander(f"🧾 Document ID: {r[0]} | Date: {r[3]}"):
            st.markdown("**Document (preview):**")
            st.code(r[1][:500] + "..." if len(r[1]) > 500 else r[1])
            st.markdown("**AI Analysis (preview):**")
            st.write(r[2][:500] + "..." if len(r[2]) > 500 else r[2])

# 3. Search Tab
with tabs[2]:
    st.header("🔍 Search Legal Docs by Keyword")
    keyword = st.text_input("Enter a keyword (e.g., termination, liability, clause)")
    if keyword:
        results = search_documents_by_keyword(keyword)
        st.markdown(f"**Found {len(results)} matches**")
        for r in results:
            with st.expander(f"📄 Document ID: {r[0]} | Date: {r[3]}"):
                st.markdown("**Document (preview):**")
                st.code(r[1][:500] + "..." if len(r[1]) > 500 else r[1])
                st.markdown("**AI Analysis (preview):**")
                st.write(r[2][:500] + "..." if len(r[2]) > 500 else r[2])

# 4. Chat with Document Tab
with tabs[3]:
    st.header("💬 Chat with Your Document")
    uploaded_chat_file = st.file_uploader("Upload a .txt or .pdf file for chatting", type=["txt", "pdf"])
    chat_document_text = ""

    if uploaded_chat_file:
        if uploaded_chat_file.type == "text/plain":
            chat_document_text = uploaded_chat_file.read().decode("utf-8")
        elif uploaded_chat_file.type == "application/pdf":
            with fitz.open(stream=uploaded_chat_file.read(), filetype="pdf") as pdf:
                text_chunks = [page.get_text() for page in pdf]
                chat_document_text = "\n".join(text_chunks)

    if chat_document_text:
        user_question = st.text_input("Ask a question about the document:")
        if user_question:
            with st.spinner("Generating response..."):
                answer = chat_with_document(chat_document_text, user_question)
            st.markdown("**Answer:**")
            st.write(answer)

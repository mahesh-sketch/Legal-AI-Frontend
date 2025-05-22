import streamlit as st
from utils import embed_document, ask_question
import fitz  # Reverted from 'import pymupdf as fitz'

st.set_page_config(page_title="GenAI Q&A", layout="centered")
st.title("🧠 GenAI Q&A Bot")
st.markdown("Upload a PDF or paste a document and ask questions using Gemini + FAISS")

st.session_state.setdefault("is_embedded", False)  # Track if document is embedded

# Helper: Extract text from PDF
def extract_text_from_pdf(file):
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text.strip()

st.subheader("📄 Upload a PDF or Paste Text Below")

uploaded_pdf = st.file_uploader("Upload a PDF document", type="pdf")
doc_input = st.text_area("Or paste your document here", height=200)

# Auto-embed if input is new and not already embedded
if uploaded_pdf and not st.session_state.is_embedded:
    with st.spinner("Extracting and embedding PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        if pdf_text:
            response = embed_document(pdf_text)
            if "error" in response:
                st.error(response["error"])
            else:
                st.success("PDF document embedded successfully!")
                st.session_state.is_embedded = True
        else:
            st.warning("The uploaded PDF has no extractable text.")

elif doc_input.strip() and not st.session_state.is_embedded:
    with st.spinner("Embedding pasted document..."):
        response = embed_document(doc_input.strip())
        if "error" in response:
            st.error(response["error"])
        else:
            st.success("Text document embedded successfully!")
            st.session_state.is_embedded = True


# Divider
st.markdown("---")

st.subheader("❓ Ask a Question")
query = st.text_input("Enter your question")

if st.button("Get Answer"):
    if not st.session_state.is_embedded:
        st.error("Please upload or paste a document first.")
    elif query.strip():
        with st.spinner("Querying..."):
            response = ask_question(query)
        if "answer" in response:
            st.success("Answer:")
            st.write(response["answer"])
        else:
            st.error("Failed to retrieve answer. Please try again.")
    else:
        st.error("Please enter a question.")

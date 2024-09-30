import streamlit as st
from transformers import BartForConditionalGeneration, BartTokenizer
import os
import difflib
import base64
import fitz  # PyMuPDF for PDF processing
from tempfile import NamedTemporaryFile

# Load pre-trained models for NER and summarization
from transformers import pipeline

ner_pipeline = pipeline("ner", grouped_entities=True)

# Load BART model and tokenizer for summarization
summarization_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
summarization_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# List of keywords to highlight with different colors
keywords = {
    "agreement": "blue",
    "party": "green",
    "confidential": "red",
    "termination": "orange",
    "liability": "purple"
}


# Function to load synthetic contracts
def load_synthetic_contracts():
    contracts = {}
    for filename in os.listdir():
        if filename.startswith("contract_") and filename.endswith(".txt"):
            with open(filename, "r") as file:
                contracts[filename] = file.read()
    return contracts


# Highlight keywords with colors
def highlight_keywords(text):
    for keyword, color in keywords.items():
        text = text.replace(keyword, f'<span style="color:{color}; font-weight:bold;">{keyword}</span>')
    return text


# Function to highlight entities in the text
def highlight_entities(text, entities):
    for entity in entities:
        word = entity['word']
        color = "yellow"
        text = text.replace(word, f'<span style="background-color:{color};">{word}</span>')
    return text


# Function to split text into chunks
def split_text(text, max_length=1024):
    sentences = text.split('. ')
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split(' '))
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            yield ' '.join(current_chunk)
            current_chunk = [sentence]
            current_length = sentence_length
    yield ' '.join(current_chunk)


# Function to summarize the contract
def summarize_contract(text):
    chunks = list(split_text(text))
    summaries = []
    for chunk in chunks:
        inputs = summarization_tokenizer.encode("summarize: " + chunk, return_tensors="pt", max_length=1024,
                                                truncation=True)
        summary_ids = summarization_model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0,
                                                   num_beams=4, early_stopping=True)
        summaries.append(summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True))
    return ' '.join(summaries)


# Function to compare two contracts and highlight differences
def compare_contracts(text1, text2):
    d = difflib.HtmlDiff()
    diff = d.make_file(text1.splitlines(), text2.splitlines())
    return diff


# Function to create download link for highlighted text
def create_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}">Download {filename}</a>'


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with fitz.open(pdf_file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# Custom CSS for styling
def custom_css():
    st.markdown("""
    <style>
    .reportview-container {
        background: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #1e1e1e;
    }
    .block-container {
        padding: 1rem;
    }
    .stButton>button {
        color: white;
        background: #444;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .stTextArea textarea {
        border: 1px solid #444;
        color: white;
        background-color: #333;
    }
    .stMarkdown {
        background-color: #333;
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    .stSidebar .stTextArea textarea, .stSidebar .stButton>button {
        background: #1e1e1e;
        color: white;
        border: 1px solid #444;
    }
    .stSidebar .stButton>button {
        background: #444;
    }
    .stSidebar {
        padding: 10px;
    }
    .top-bar {
        background: #333;
        color: white;
        padding: 10px 0;
        text-align: center;
        font-size: 24px;
        width: 100%;
        top: 0;
        z-index: 1000;
        border-bottom: 2px solid #444;
    }
    .main-content {
        padding-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)


# Function to display the top bar
def display_top_bar():
    st.markdown("""
    <div class="top-bar">Business Contract Validator</div>
    """, unsafe_allow_html=True)


# Main content display
def display_main_content():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)


def main():
    custom_css()
    display_top_bar()
    display_main_content()

    st.sidebar.title("Options")

    # Load synthetic contracts
    synthetic_contracts = load_synthetic_contracts()

    # Select synthetic contract
    selected_contract = st.sidebar.selectbox("Select a synthetic contract", list(synthetic_contracts.keys()))
    uploaded_file = st.sidebar.file_uploader("Upload your own contract", type=["txt", "pdf"])

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            # Read the content of the uploaded text file
            contract_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            # Save the uploaded file to a temporary location
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_file_path = temp_file.name
            # Extract text from the uploaded PDF file
            contract_text = extract_text_from_pdf(temp_file_path)
    elif selected_contract:
        # Use the selected synthetic contract
        contract_text = synthetic_contracts[selected_contract]
    else:
        contract_text = None

    if contract_text:
        # Use columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Contract")
            st.text_area("Contract Text", contract_text, height=300)

        with col2:
            st.subheader("Contract Summary")
            summary = summarize_contract(contract_text)
            st.markdown(f'<div class="stMarkdown">{summary}</div>', unsafe_allow_html=True)

        st.subheader("Highlighted Contract")
        highlighted_text = highlight_keywords(contract_text)
        entities = ner_pipeline(contract_text)
        highlighted_text_with_entities = highlight_entities(highlighted_text, entities)
        st.markdown(highlighted_text_with_entities, unsafe_allow_html=True)

        st.subheader("Entities Detected")
        for entity in entities:
            st.markdown(
                f"**Entity**: {entity['word']} **Label**: {entity['entity_group']} **Score**: {entity['score']:.2f}")

        st.subheader("Compare with Another Contract")
        other_uploaded_file = st.file_uploader("Upload another contract for comparison", type=["txt", "pdf"],
                                               key="compare")
        if other_uploaded_file is not None:
            try:
                if other_uploaded_file.type == "text/plain":
                    other_contract_text = other_uploaded_file.read().decode("utf-8")
                elif other_uploaded_file.type == "application/pdf":
                    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(other_uploaded_file.getbuffer())
                        temp_file_path = temp_file.name
                    other_contract_text = extract_text_from_pdf(temp_file_path)

                comparison_result = compare_contracts(contract_text, other_contract_text)
                st.subheader("Comparison Result")
                st.markdown(comparison_result, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error comparing contracts: {e}")

        st.subheader("Download Highlighted Contract")
        download_link = create_download_link(highlighted_text_with_entities, "highlighted_contract.html")
        st.markdown(download_link, unsafe_allow_html=True)

        st.sidebar.subheader("User Feedback")
        feedback = st.sidebar.text_area("Please provide your feedback on the analyzed contract:")
        if st.sidebar.button("Submit Feedback"):
            st.sidebar.write("Thank you for your feedback!")

    # Close main content div
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()

    main()



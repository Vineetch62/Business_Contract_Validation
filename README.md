# Business_Contract_Validation

This project is a Streamlit app that highlights important parts of contracts and identifies specific entities (like names or dates). It classifies contract clauses, checks for differences from a standard template, and marks those differences.



## Features

- Automatically extracts and categorizes contract sections.
- Highlights important details like dates, parties, and legal terms.
- Spots differences from standard contract templates.
- Gives a quick summary of the contract.
- Allows downloading the highlighted contract as a PDF or DOCX file.




## Technology Used

- **PyMuPDF:** For PDF text extraction.
- **Transformers (Huggingface):** For Named Entity Recognition (NER).
- **Streamlit:** For the interactive web application.
- **Difflib:** For comparing contract texts.


## Installation
### Prerequisites
- Python 3.7 or higher
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Vineetch62/Business_Contract_Validation.git
    cd Business_Contract_Validation
   ```
   
2. Create a virtual environment and activate it:
   - Windows
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   - MacOs
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```bash
      streamlit run contractapp.py
   ```
2. Open your web browser and go to `http://localhost:8501` to access the application.

## Project Strucure

```plaintext
Business-Contract-Validation/
├── contractapp.py
├── generate.py
├── requirements.txt
├── README.md
├── contracts/
│   ├── contract_1.txt
│   ├── contract_2.txt
│   ├── contract_3.txt
│   ├── contract_4.txt
└── Demonstration

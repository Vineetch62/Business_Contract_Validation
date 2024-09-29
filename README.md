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



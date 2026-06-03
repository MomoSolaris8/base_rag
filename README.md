# base_rag

A basic RAG learning project built with Python, Streamlit, LangChain, DashScope,
and ChromaDB.

This project is currently used to learn:

- how to upload text files with Streamlit
- how to calculate MD5 values for text
- how to avoid processing the same content more than once
- how to build a basic knowledge base for RAG

## Requirements

- Python 3.10 or newer
- pip
- A virtual environment is recommended

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

If you do not want to use `requirements.txt`, you can also install the packages
manually:

```bash
pip install streamlit langchain langchain-community dashscope chromadb
```

## Run

Run the Streamlit file uploader app:

```bash
streamlit run app_file_uploader.py
```

Run the knowledge base script:

```bash
python knowledge_base.py
```

## Project Structure

```text
base_rag/
├── app_file_uploader.py   # Streamlit file upload page
├── app_qa.py              # Question-answering app
├── config_data.py         # Project configuration
├── knowledge_base.py      # Knowledge base and MD5 logic
├── md5.text               # Stores processed MD5 values
├── rag.py                 # RAG logic
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Notes

`md5.text` is used to store MD5 values that have already been processed. This
helps the project check whether incoming text has been handled before.

The project uses `utf-8` when reading and writing text so that English, Chinese,
German characters such as `ä`, `ö`, `ü`, and other Unicode text can be handled
correctly.

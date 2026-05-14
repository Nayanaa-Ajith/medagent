import os
from dotenv import load_dotenv
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

def load_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_text(text)

def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local("vectorstore")
    print(f"✅ Vectorstore created with {len(chunks)} chunks!")

def ingest(file_path):
    print(f"📄 Loading PDF: {file_path}")
    text = load_pdf(file_path)
    print(f"✅ Extracted {len(text)} characters")
    chunks = split_text(text)
    print(f"✅ Created {len(chunks)} chunks")
    create_vectorstore(chunks)

if __name__ == "__main__":
    ingest("data/medical.pdf")
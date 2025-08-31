from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
import shutil
import os


data_path = "data"
vt_data_path = "db_faiss"



def create_vector_store():
  loader = DirectoryLoader(data_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
  documents = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
  chunks = text_splitter.split_documents(documents)

  embedding_model = GPT4AllEmbeddings(model_file="C:\\Users\\Admin\\Desktop\\RAG_demo\\models\\all-MiniLM-L6-v2-f16.gguf")
  db = FAISS.from_documents(chunks, embedding_model)
  db.save_local(vt_data_path)
  return db


print(1)
db = create_vector_store()
print(1)
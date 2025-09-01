from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

vt_data_path = "C:\\Users\\Admin\\PycharmProjects\\Student_Manager\\app\\services\\RAG\\db_faiss"

class GeminiLLM:
    """Custom LLM wrapper for Gemini"""

    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate(self, prompt):
        """Generate response from Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

def read_from_db():
    """Load FAISS vector database"""
    try:
        embedding = GPT4AllEmbeddings(
            model_file="C:\\Users\\Admin\\Desktop\\RAG_demo\\models\\all-MiniLM-L6-v2-f16.gguf"
        )
        db = FAISS.load_local(vt_data_path, embedding, allow_dangerous_deserialization=True)
        return db
    except Exception as e:
        print(f"Error loading database: {e}")
        return None

# Template for RAG
template = """Bạn là một trợ lý AI thông minh. Sử dụng thông tin bối cảnh dưới đây để trả lời câu hỏi một cách chính xác và hữu ích.

Bối cảnh:
{context}

Câu hỏi: {question}

Hướng dẫn:
- Trả lời dựa trên thông tin được cung cấp trong bối cảnh
- Nếu không phải là câu hỏi về thông tin, hãy giới thiệu mình là chatbot của Học viện Công nghệ Bưu chính Viễn thông
- Trả lời bằng tiếng Việt
- Cung cấp câu trả lời rõ ràng và hữu ích

Trả lời:"""

class RAGChain:
    """Custom RAG chain for Gemini"""

    def __init__(self, llm, db, template):
        self.llm = llm
        self.db = db
        self.template = template

    def run(self, query):
        """Run RAG query"""
        try:
            # Retrieve relevant documents
            docs = self.db.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in docs])

            # Format prompt
            formatted_prompt = self.template.format(context=context, question=query)

            # Generate response using Gemini
            response = self.llm.generate(formatted_prompt)
            return response
        except Exception as e:
            return f"Error processing query: {str(e)}"

def load_model():
    """Load complete RAG model"""
    try:
        print("Loading vector database...")
        db = read_from_db()
        if db is None:
            print("Failed to load vector database")
            return None

        print("Initializing Gemini model...")
        llm = GeminiLLM()

        print("Creating RAG chain...")
        rag_chain = RAGChain(llm=llm, db=db, template=template)

        print("RAG model loaded successfully")
        return rag_chain
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Test function
def response(query):
    """Test RAG functionality"""
    chain = load_model()
    if chain:
        response = chain.run(query)
        print(f"Response: {response}")
        return response
    else:
        print("Failed to load RAG model")
        return None

import os
import chromadb
from google import genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# ==========================================
# 1. Initialization & Security Setup
# ==========================================
print("Loading secure environment variables...")
load_dotenv()  # Reads the .env file
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY not found in .env file!")

# Initialize the NEW GenAI Client (Modern Instance-based approach)
ai_client = genai.Client(api_key=API_KEY)

# Initialize Vector DB & Embedding Model
print("Initializing Embedding Model and Vector DB...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_collection(name="costco_products")

# ==========================================
# 2. Core RAG Pipeline (Retrieval -> Generation)
# ==========================================
def generate_shopping_advice(user_query):
    print(f"Vectorizing query: '{user_query}'")
    query_vector = embedding_model.encode(user_query).tolist()
    
    print("Retrieving context from ChromaDB...")
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )

    # 3. Context Construction & Distance Thresholding
    context_str = ""
    valid_items_count = 0
    DISTANCE_THRESHOLD = 1.4
    
    for i in range(len(results['ids'][0])):
        dist = results['distances'][0][i]
        if dist <= DISTANCE_THRESHOLD:
            meta = results['metadatas'][0][i]
            context_str += f"- Product: {meta['name']} | Brand: {meta['brand']} | Price: ${meta['price']}\n"
            valid_items_count += 1

    # 4. Prompt Engineering
    if valid_items_count == 0:
        prompt = (
            f"The user asked for: '{user_query}'. "
            f"Our database returned NO relevant products. "
            f"Politely apologize as an AI-Mart assistant, and suggest they browse our trending Costco items instead."
        )
    else:
        prompt = f"""
        You are a highly professional and enthusiastic AI shopping assistant for AI-Mart (a Costco-themed e-commerce platform).
        
        The user asked: "{user_query}"
        
        Here is the FACTUAL CONTEXT retrieved from our inventory database:
        {context_str}
        
        INSTRUCTIONS:
        1. Based ONLY on the factual context provided above, recommend the products to the user.
        2. Explain briefly why these specific items fit their request.
        3. Highlight the Costco-style value (e.g., bulk sizing, Kirkland quality) if applicable.
        4. Do NOT invent or hallucinate products that are not in the context list.
        5. Keep the tone friendly, concise, and helpful.
        """

    print("Generating AI response via modern GenAI SDK...\n")
    # Using the new Client method and recommending the latest flash model
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

# ==========================================
# 3. Execution
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("🚀 AI-Mart Modern RAG Engine Started")
    print("="*50)
    
    test_query = "I need to buy A shirt to wear in Seattle."
    print(f"USER: {test_query}\n")
    
    final_answer = generate_shopping_advice(test_query)
    
    print("🤖 AI-MART ASSISTANT:")
    print(final_answer)
    print("="*50)
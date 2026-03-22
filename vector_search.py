import json
import chromadb
from sentence_transformers import SentenceTransformer

def main():
    print("Initializing ChromaDB Persistent Client...")
    # This will create a folder named 'chroma_data' in project
    # to store the vector database permanently on hard drive.
    client = chromadb.PersistentClient(path="./chroma_data")
    
    collection_name = "costco_products"
    
    # Clean slate for our tutorial: delete if it already exists
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    # Create the collection (think of it as a Table in traditional SQL)
    collection = client.create_collection(name=collection_name)
    print(f"Collection '{collection_name}' ready.\n")

    print("Loading products_with_vectors.json...")
    with open("products_with_vectors.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    # Prepare data arrays for ChromaDB bulk insertion
    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for p in products:
        ids.append(str(p["id"]))
        # We pass the pre-computed 384-dimensional vector from Day 2
        embeddings.append(p["embedding_vector"])
        documents.append(p["description"])
        
        # SDE-AI Core Concept: Separating Structured Data into Metadata
        # We keep price and category here for future Hybrid Search pre-filtering!
        metadatas.append({
            "name": p["name"],
            "category": p["category"],
            "price": p["price"],
            "brand": p["attributes"]["brand"]
        })

    print(f"Inserting {len(ids)} products into the Vector DB...")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print("Insertion complete!\n")

    # ==========================================
    # 🎯 TEST: SEMANTIC SEARCH IN ACTION
    # ==========================================
    print("-" * 40)
    print("TESTING SEMANTIC SEARCH")
    print("-" * 40)
    
    user_query = "I need something for a weekend camping trip"
    print(f"User asks: '{user_query}'\n")
    
    # 1. We MUST use the EXACT SAME model to embed the user's query
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode(user_query).tolist()

    # 2. Perform the Vector Search (ANN - Approximate Nearest Neighbor)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3  # Return the top 3 closest matches
    )

    print("Evaluating Semantic Matches...\n")
    
    # Distance Thresholding (Confidence Filtering)
    # For L2 distance in ChromaDB with all-MiniLM-L6-v2, 
    # distances > 1.2 usually mean poor semantic relation.
    DISTANCE_THRESHOLD = 1.2 
    valid_results_found = False

    for i in range(len(results['ids'][0])):
        match_id = results['ids'][0][i]
        match_meta = results['metadatas'][0][i]
        match_dist = results['distances'][0][i]
        
        # Check if the result passes our strict confidence threshold
        if match_dist <= DISTANCE_THRESHOLD:
            valid_results_found = True
            print(f"✅ Match Rank {i+1} | ID: {match_id} (Passes Threshold)")
            print(f"Product : {match_meta['name']}")
            print(f"Brand   : {match_meta['brand']}")
            print(f"Price   : ${match_meta['price']}")
            print(f"Distance: {match_dist:.4f}") 
            print("-" * 20)
        else:
            # We silently ignore or log the garbage results
            print(f"❌ Rejected Rank {i+1} | ID: {match_id} (Distance {match_dist:.4f} > {DISTANCE_THRESHOLD})")

    # The Graceful Fallback (Degradation Strategy)
    if not valid_results_found:
        print("\n⚠️ SYSTEM ALERT: No highly relevant products found.")
        print("Fallback Triggered: Displaying 'Global Top Trending Items' instead.")
        # In a real system, you would call a function like get_trending_products() here.

if __name__ == "__main__":
    main()
import json
import time
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    # Using a lightweight, widely adopted English embedding model.
    # It converts any text into a 384-dimensional vector.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded successfully.\n")

    print("Reading products.json...")
    try:
        with open("products.json", "r", encoding="utf-8") as file:
            products = json.load(file)
    except FileNotFoundError:
        print("Error: products.json not found. Please run data_generator.py first.")
        return

    print(f"Starting vectorization for {len(products)} products...")
    start_time = time.time()

    for product in products:
        # SDE-AI Core Concept: Context Enrichment
        # We concatenate the product name and description to provide maximum semantic value for the model.
        text_context = f"{product['name']}. {product['description']}"
        
        # model.encode generates the dense vector. We convert it to a standard Python list.
        vector = model.encode(text_context).tolist()
        
        # Attach the vector back to the product dictionary
        product['embedding_vector'] = vector

    elapsed_time = round(time.time() - start_time, 2)
    print(f"Vectorization completed in {elapsed_time} seconds.\n")

    output_filename = "products_with_vectors.json"
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=2)

    print(f"Success! Data saved to {output_filename}.")

if __name__ == "__main__":
    generate_embeddings()
import json
import random

# Costco-style Data Vocabulary
brands = ["Kirkland Signature", "Ninja", "Dyson", "Samsung", "LG", "Bose", "Tropicana"]
categories = {
    "Electronics": ["4K Ultra HD", "Noise Cancelling", "Smart Home Integration", "Wireless", "OLED Display"],
    "Home & Kitchen": ["Energy Efficient", "High Power", "Stainless Steel", "Bagless", "Multi-functional"],
    "Groceries": ["Organic", "Bulk Pack", "Gluten-Free", "Non-GMO", "Family Size"],
    "Apparel": ["Merino Wool", "Water-Resistant", "Breathable", "Four-Way Stretch", "Fleece Lined"]
}
package_types = ["Value Pack", "Warehouse Club Size", "2-Pack", "30-Count", "Gallon"]
features = ["Exclusive Member Pricing", "Extended Warranty", "Premium Quality", "Everyday Value"]

def generate_costco_products(num=50):
    products = []
    for i in range(1, num + 1):
        category = random.choice(list(categories.keys()))
        brand = random.choice(brands)
        key_spec = random.choice(categories[category])
        package = random.choice(package_types)
        feature = random.choice(features)
        
        # Override brand for Groceries to make it more Costco-authentic
        if category == "Groceries" and random.random() > 0.5:
            brand = "Kirkland Signature"
            
        name = f"{brand} {key_spec} {category[:-1] if category.endswith('s') else category} - {package}"
        
        # English description optimized for LLM/Vector search
        description = (
            f"Experience {feature.lower()} with the {name}. "
            f"Designed for your {category.lower()} needs, this product features {key_spec.lower()} technology/ingredients. "
            f"Sold in a convenient {package.lower()}, making it perfect for stocking up your home or office. "
            f"Backed by our 100% satisfaction guarantee."
        )
        
        # Pricing logic based on category
        if category == "Electronics":
            price = round(random.uniform(199.99, 1499.99), 2)
        elif category == "Groceries":
            price = round(random.uniform(9.99, 49.99), 2)
        else:
            price = round(random.uniform(29.99, 299.99), 2)
            
        product = {
            "id": i,
            "name": name,
            "category": category,
            "price": price,
            "attributes": {
                "brand": brand,
                "package_size": package,
                "key_specification": key_spec,
                "member_benefit": feature
            },
            "description": description
        }
        products.append(product)
    return products

if __name__ == "__main__":
    print("Initializing Costco-style mock data generation...")
    # Generate 50 items
    mock_data = generate_costco_products(50)
    
    # Save to JSON
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated {len(mock_data)} products. Saved to products.json!")
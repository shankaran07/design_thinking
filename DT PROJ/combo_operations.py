import random
from flask import current_app
from itertools import combinations

def fetch_products_for_combo(budget, category=""):
    """
    Fetch the products from MongoDB that fit within the user's budget and category.
    """
    # Access the products collection from the Flask app context
    products_collection = current_app.config["MONGO_DB"]["products"]

    query = {"price": {"$lte": budget}}  # Query for products within budget
    if category:
        query["category"] = category  # Add category filter if provided

    # Fetch products from MongoDB
    products = products_collection.find(query)
    
    # Create a list of products to return
    product_list = [
        {
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "category": product["category"],
            "rating": product.get("rating", 0),  # Default to 0 if rating is missing
            "shop_id": product["shop_id"],
            "image_url": product.get("image_url", ""),  # Default to empty string if no image URL
        }
        for product in products
    ]
    
    print(f"Fetched Products: {product_list}")  # Debugging line
    return product_list



def generate_combos(products, budget):
    """
    Generate all possible combinations of products that fit within the given budget.
    """
    if not products or budget <= 0:  # Base case: no products or budget exhausted
        return []

    # List to hold all valid combinations
    valid_combos = []

    # Generate all combinations of products
    for r in range(1, len(products) + 1):  # Generate combos of all sizes
        for combo in combinations(products, r):
            total_price = sum(product['price'] for product in combo)

            if total_price <= budget:  # Only keep combos that fit within the budget
                valid_combos.append(list(combo))  # Store as a list of products

    # Debugging line
    print(f"Generated Combos: {valid_combos}")
    return valid_combos




def rank_combos(combos):
    """
    Rank the combos based on product ratings, shop diversity, and price balance.
    """
    def combo_score(cmb):
        """
        Calculate the score for a combo based on the following criteria:
        - Sum of ratings of the products in the combo.
        - Shop diversity: the number of unique shops in the combo.
        """
        if isinstance(cmb, list):  # Ensure the combo is a list of dictionaries (products)
            rating_sum = sum(product["rating"] for product in cmb)
            shop_diversity = len(set(product["shop_id"] for product in cmb))
            return rating_sum + shop_diversity
        else:
            print("Error: Combo contains non-list elements!")  # Debugging line
            return 0

    print(f"Ranking Combos: {combos}")  # Debugging line
    return sorted(combos, key=combo_score, reverse=True)

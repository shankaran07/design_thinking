from pymongo import MongoClient
import urllib.parse

# MongoDB connection setup
username = "shriraamsj21"
password = "Sharan@123"
encoded_password = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{encoded_password}@cluster21.jhxmf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Define database and collection
db = client.get_database("vishaal_de_mall")
products_collection = db["products"]

# Sample dataset
sample_data = [
    {
        "name": "Smartphone",
        "price": 500,
        "category": "electronics",
        "shop_id": "shop1",
        "image_url": "https://via.placeholder.com/100",
    },
    {
        "name": "Headphones",
        "price": 200,
        "category": "electronics",
        "shop_id": "shop2",
        "image_url": "https://via.placeholder.com/100",
    },
    {
        "name": "Charger",
        "price": 100,
        "category": "electronics",
        "shop_id": "shop3",
        "image_url": "https://via.placeholder.com/100",
    },
    {
        "name": "Laptop Bag",
        "price": 300,
        "category": "accessories",
        "shop_id": "shop4",
        "image_url": "https://via.placeholder.com/100",
    },
]

# Insert the sample data
if products_collection.count_documents({}) == 0:  # Avoid duplicate insertion
    products_collection.insert_many(sample_data)
    print("Sample data inserted successfully.")
else:
    print("Products collection already contains data.")

client.close()

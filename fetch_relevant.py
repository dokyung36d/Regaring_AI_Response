from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from key import mongodb_password

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['RAG']
collection = db['embedding']

if __name__ == "__main__":
    # Fetch one document
    document = collection.find_one()
    hobby_embedding = document["hobby_embedding"]

    pipeline = [
        {
            "$addFields": {
                "dot_product": {
                    "$let": {
                        "vars": {
                            "query": hobby_embedding,
                            "embedding": "$hobby_embedding"
                        },
                        "in": {
                            "$reduce": {
                                "input": {"$range": [0, {"$size": "$$query"}]},
                                "initialValue": 0,
                                "in": {
                                    "$add": [
                                        "$$value",
                                        {
                                            "$multiply": [
                                                {"$arrayElemAt": ["$$query", "$$this"]},
                                                {"$arrayElemAt": ["$$embedding", "$$this"]}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        {"$sort": {"dot_product": -1}},  # Sort by highest similarity
        {"$limit": 3}  # Limit to top 3
    ]

    # Execute the aggregation
    results = list(collection.aggregate(pipeline))

    print(f"{document['name']}'s hobby : {document['hobby']}")

    # Display the results
    for result in results:
        print(f"Fetched {result['name']}'s hobby : {result['hobby']}")

def fetch_relevant_document(embedding):
    pipeline = [
        {
            "$addFields": {
                "dot_product": {
                    "$let": {
                        "vars": {
                            "query": embedding,
                            "embedding": "$hobby_embedding"
                        },
                        "in": {
                            "$reduce": {
                                "input": {"$range": [0, {"$size": "$$query"}]},
                                "initialValue": 0,
                                "in": {
                                    "$add": [
                                        "$$value",
                                        {
                                            "$multiply": [
                                                {"$arrayElemAt": ["$$query", "$$this"]},
                                                {"$arrayElemAt": ["$$embedding", "$$this"]}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        {"$sort": {"dot_product": -1}},  # Sort by highest similarity
        {"$limit": 3}  # Limit to top 3
    ]

    # Execute the aggregation
    results = list(collection.aggregate(pipeline))

    retrieved_name_list = []
    retrieved_hobby_list = []

    # Display the results
    for result in results:
        #print(f"Fetched {result['name']}'s hobby : {result['hobby']}")
        retrieved_name_list.append(result["name"])
        retrieved_hobby_list.append(result["hobby"])

    return retrieved_name_list, retrieved_hobby_list
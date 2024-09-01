from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import ast
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class MongodbTool:
    def __init__(self, connection_string, database_name):
        self.mongo_url = connection_string
        self.client = MongoClient(self.mongo_url)
        self.db_name = database_name
        # Connect to MongoDB
        try:
            self.client.admin.command("ismaster")
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            exit()

    def parse_query(self, query_string):
        # Example query string
        # query_string = 'db.smart_test.find({ "selling_price": { "$lt": 200 } })'

        # Extract the collection name
        collection_name = query_string.split(".")[1].split(".find")[0]

        # Extract the dictionary part of the query string
        query_dict_str = query_string[
            query_string.find("{") : query_string.rfind("}") + 1
        ]

        # Safely evaluate the string to convert it into a Python dictionary
        query_dict = ast.literal_eval(query_dict_str)
        return collection_name, query_dict

    def run(self, query_string):
        """
        Fetch data from MongoDB based on the provided query.
        """
        collection_name, query_dict = self.parse_query(query_string)
        db = self.client[self.db_name]
        collection = db[collection_name]
        result = collection.find(query_dict)
        return list(result)

class RetriverAgent:
    def __init__(self):
        pass

    def run(self, user_input):
        database_info = """
        Database_name: disha_fashion
        Collection_name: store_analysis
        """
        schema_example = """
        _id: ['ObjectId']
        store_id: ['ObjectId']
        name: ['str']
        capture_count: ['int']
        beauty_capture_count: ['int']
        osa: ['float']
        beauty_osa: ['int', 'float']
        anomaly_count: ['int']
        beauty_anomaly_count: ['int']
        vm: ['float']
        capture_percentage: ['float']
        beauty_capture_percentage: ['int', 'float']
        timestamps: ['datetime']
        """
        prompt = f"""
        You are an AI assistant that converts natural language instructions into MongoDB queries.
        Database Information: {database_info}
        Schema example: {schema_example}
        Example:
        Input: "give me the list of product only that have discount greater than 500"
        Output: db.collection_name{{ "discount": {{ "$gt": 500 }} }}

        Input: {user_input}
        Output:
        """
        # print(prompt)
        return prompt


class CognitiveAgent:
    def _init_(self):
        pass

    def run(self, user_input, query_result):
        prompt = f"""
        You are an AI assistant that converts MongoDB query results into human-readable natural language responses based on the question asked.
        Example:
        Input:
        question : list of stores with capture count greater then 50
        data : [{{'_id': ObjectId('66bc422ab02a0f30e499b362'), 'store_id': ObjectId('665598dae2c81415d464c64c'), 'name': 'BB-GHAZIABAD-OPULENT MALL-ED', 'capture_count': 68, 'beauty_capture_count': 10, 'osa': 99.83661764705883, 'beauty_osa': 49.375, 'anomaly_count': 19, 'beauty_anomaly_count': 2, 'vm': 72.05882352941177, 'capture_percentage': 100.0, 'beauty_capture_percentage': 100.0, 'timestamps': datetime.datetime(2024, 8, 2, 0, 0)}}, {{'_id': ObjectId('66bc422bb02a0f30e499b3c8'), 'store_id': ObjectId('6655a6f7b7950d9c3333f9e2'), 'name': 'BB- MAHAGUN MALL-GHAZIABAD', 'capture_count': 136, 'beauty_capture_count': 0, 'osa': 100.0, 'beauty_osa': 0, 'anomaly_count': 21, 'beauty_anomaly_count': 0, 'vm': 84.55882352941177, 'capture_percentage': 100.0, 'beauty_capture_percentage': 0, 'timestamps': datetime.datetime(2024, 8, 2, 0, 0)}}]
        Output: "I found 2 stores with capture count greater then 50:
        BB-GHAZIABAD-OPULENT MALL-ED, capture_count is 68
        BB- MAHAGUN MALL-GHAZIABAD, capture_count is 136."

        Input: question: {user_input}, data: {query_result}
        Output:
        """
        return prompt
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
        """
        prompt = f"""
        You are an AI assistant that converts natural language instructions into MongoDB queries.
        Database Information: {database_info}
        Schema example: {schema_example}
        Example:
        Input: 
        Output: 

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
        question : 
        data : 
        Output: 

        Input: question: {user_input}, data: {query_result}
        Output:
        """
        return prompt

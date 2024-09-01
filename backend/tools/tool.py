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


class OllamaTool:
    def __init__(self, model_name):
        self.model_name = model_name

    def run(self, prompt):
        """
        Perform task as assigned by the agents using the Ollama model.

        Args:
            prompt (str): The input prompt to process.

        Returns:
            str: The processed output from the model.
        """
        # Use the Ollama API or the appropriate Ollama Python client for text generation
        import subprocess

        command = f"ollama generate {self.model_name} --prompt '{prompt}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to generate text: {result.stderr}")
        return result.stdout.strip()

class RetriverAgent:
    def __init__(self, llm_tool):
        # print(llm_tool)
        self.llm_tool = llm_tool

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
        return self.llm_tool.run(prompt)


class ChatbotPipeline:
    def __init__(self, retriver_agent, mongo_tool):
        self.retriver_agent = retriver_agent
        self.mongo_tool = mongo_tool
        # self.cognitive_agent = cognitive_agent

    def run(self, user_input):
        # Step 1: Convert natural language to MongoDB query
        mongo_query = self.retriver_agent.run(user_input)
        print(f"Generated MongoDB Query: {mongo_query}")

        # Step 2: Fetch data from MongoDB using the generated query
        result = self.mongo_tool.run(mongo_query)
        if len(result) > 10:
            result = result[0:10]
        print(f"Fetched Result: {result}")

        # Step 3: Convert the MongoDB result to a natural language response
        # natural_language_response = self.cognitive_agent.run(user_input, str(result))
        return result
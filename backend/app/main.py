from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from tools.tool import MongodbTool, RetriverAgent, CognitiveAgent

OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

llm = Ollama(model="phi3", temperature=0, base_url=OLLAMA_BASE_URL)
llm2 = Ollama(model="phi3", temperature=0, base_url="127.0.0.1:8000")
# llm._generate("How's the weather today..?")


retrievePrompt = RetriverAgent()
CognitiveAgentPrompt = CognitiveAgent()

app = FastAPI()

class Message(BaseModel):
    text: str

origins = [
    "*",
    "http://localhost:6434/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/messages")
async def get_initial_message():
    return {"message": "Hello!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text_data = await websocket.receive_text()
            input = text_data
            print(input)
            query = retrievePrompt.run(input)
            print(query)
            # print(response)
            lst = ""

            for chunks in llm.stream(query):
                lst = lst+ chunks

            print(lst)
            response = mongo_tool.run(query_string=lst)

            cognitivePrompt =  CognitiveAgentPrompt.run(input, response[:4])
            print(cognitivePrompt)
            final = ""
            for chunks in llm2.stream(cognitivePrompt):
                await websocket.send_text(chunks)
            await websocket.send_text('**|||END|||**')
    except Exception as e:
        print(f'WebSocket error: {str(e)}')
    finally:

        await websocket.close()
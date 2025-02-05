from fastapi import FastAPI # type: ignore
from chat_agent import generate_response

app = FastAPI()

@app.get("/chat/")
async def chat(query: str):
    response = generate_response(query)
    return {"response": response}

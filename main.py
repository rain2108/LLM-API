from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import uvicorn
from pydantic import BaseModel
import requests
from llm2 import get_llm_response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to a list of allowed origins in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_llm(request: QueryRequest):
    try:
        # Call your LLM function with the user-provided query
        answer = get_llm_response(request.query)
        return {"answer": answer}
    except Exception as e:
        # If something goes wrong, return a 500 error with the error details
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    # Start ngrok and get the public URL
    public_url = ngrok.connect(8000)
    print("Public URL:", public_url)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
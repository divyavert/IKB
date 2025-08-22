from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from ikb_backend.llm import get_answer

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PromptRequest(BaseModel):
    prompt: str
    context: str

@app.post("/v1/chat")
async def process_prompt(request: PromptRequest):
    prompt = request.prompt
    context = request.context
    answer = get_answer(prompt)
    return {"message": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
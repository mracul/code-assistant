from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from context_engine import input_handler, file_discovery, tokenization

app = FastAPI()

class AnalyzeRequest(BaseModel):
    prompt: str
    path: str

@app.get("/api/v1/ping")
def read_root():
    return {"status": "ok"}

@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):
    try:
        input_handler.validate_path(request.path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    discovered_files = list(file_discovery.discover_files(request.path))

    tokenizer = tokenization.get_tokenizer()

    file_summaries = []
    for file_path in discovered_files:
        content = tokenization.read_file_content(file_path)
        token_count = tokenization.count_tokens(content, tokenizer)
        chunks = list(tokenization.chunk_content(content, tokenizer))
        file_summaries.append({
            "path": file_path,
            "token_count": token_count,
            "num_chunks": len(chunks)
        })

    return {
        "status": "ok",
        "message": f"Analyzed {len(file_summaries)} files from '{request.path}'.",
        "files": file_summaries
    }
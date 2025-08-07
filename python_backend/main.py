from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from context_engine import input_handler, file_discovery, tokenization, vector_store

app = FastAPI()

# Create a global in-memory vector store instance
db = vector_store.InMemoryVectorStore()

class AnalyzeRequest(BaseModel):
    prompt: str
    path: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

@app.get("/api/v1/ping")
def read_root():
    return {"status": "ok"}

@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):
    try:
        input_handler.validate_path(request.path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Clear the old store for a fresh analysis
    db.clear()

    discovered_files = list(file_discovery.discover_files(request.path))
    tokenizer = tokenization.get_tokenizer()

    total_chunks_embedded = 0
    for file_path in discovered_files:
        content = tokenization.read_file_content(file_path)
        if not content or content.startswith("Error reading file"):
            continue

        chunks_text = list(tokenization.chunk_content(content, tokenizer))
        if not chunks_text:
            continue

        embeddings = vector_store.generate_embeddings(chunks_text)
        if not embeddings:
            continue

        # Prepare metadata
        metadata = [
            {"file_path": file_path, "chunk_id": i, "content": chunk}
            for i, chunk in enumerate(chunks_text)
        ]

        db.add(embeddings, metadata)
        total_chunks_embedded += len(chunks_text)

    return {
        "status": "ok",
        "message": f"Analyzed {len(discovered_files)} files and stored {total_chunks_embedded} embedding chunks in memory.",
    }

@app.post("/api/v1/search")
def search(request: SearchRequest):
    try:
        query_embedding = vector_store.generate_embeddings([request.query])
        if not query_embedding:
            return {"status": "ok", "results": []}

        search_results = db.search(query_embedding[0], k=request.limit)
        return {
            "status": "ok",
            "results": search_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
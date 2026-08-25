from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from nlp_engine.analyzer import GermanNLPEngine

app = FastAPI(
    title="DeutschNLP Studio API",
    description="Full-stack German Natural Language Processing Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GermanNLPEngine()

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="German text payload")

@app.post("/api/analyze")
async def analyze_text(payload: AnalysisRequest):
    try:
        results = engine.analyze(payload.text)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static web client
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
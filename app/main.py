import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from .rag import retrieve_context


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str


async def call_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "http://llm:11434/v1/chat/completions",
            json={
                "model": "qwen2.5:3b",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
            },
        )
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/ask", response_model=Answer)
async def ask(q: Question) -> Answer:
    results = retrieve_context(q.question)
    chunks = []

    for node in results:
        title = node.metadata.get("title") or "Unknown title"
        artist = node.metadata.get("artist") or "Unknown artist"
        album = node.metadata.get("album") or "Unknown album"
        chunks.append(f"{title} by {artist} from {album}:\n{node.text}")

    context = "\n\n".join(chunks)

    prompt = f"""
    You are analyzing song lyrics.

    Use ONLY the provided lyrics below to answer the question.
    If multiple songs are relevant, compare them and mention each song explicitly. 
    Use the song's metadata to determine the song's title, album (if appliccable) and artist.
    
    Lyrics:
    {context}

    Question:
    {q.question}

    Answer:
    """  # noqa

    answer = await call_llm(prompt)
    return Answer(answer=answer)

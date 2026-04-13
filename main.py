from fastapi import FastAPI
from pydantic import BaseModel
from rag import retrieve_context


class Question(BaseModel):
    question: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/ask")
async def ask(q: Question):
    results = retrieve_context(q.question)

    context = "\n\n".join(
        f"{node.metadata.get('title')} by {node.metadata.get('artist')}:\n{node.text}"
        for node in results
    )

    prompt = f"""
    You are analyzing song lyrics.

    Use the lyrics below to answer the question.
    If multiple songs are relevant, compare them and mention each song explicitly. 
    Use the song's metadata determine the song's title, album (if appliccable) and artist.
    
    Lyrics:
    {context}

    Question:
    {q.question}

    Answer:
    """

    return {"prompt": prompt}

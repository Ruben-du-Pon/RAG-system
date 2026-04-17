from fastapi import FastAPI

app = FastAPI()


@app.post("/v1/chat/completions")
async def fake_completion():
    return {
        "choices": [{"message": {"content": "This is a fake LLM response"}}]
    }

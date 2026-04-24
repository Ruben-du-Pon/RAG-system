# Song Lyrics RAG API

A Retrieval-Augmented Generation (RAG) API for querying song lyrics using natural language. Ask questions about lyrics and get answers grounded in the actual song content.

## How It Works

1. Song lyrics are loaded from the `app/data/` directory at startup and indexed using vector embeddings ([BAAI/bge-small-en](https://huggingface.co/BAAI/bge-small-en) via HuggingFace).
2. When a question is submitted, the most relevant lyric chunks are retrieved from the index.
3. The retrieved lyrics and the question are sent as a prompt to a local LLM ([Qwen 2.5 3B](https://ollama.com/library/qwen2.5) via Ollama).
4. The LLM returns an answer based solely on the provided lyrics.

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI app and LLM call logic
│   ├── rag.py           # Document loading, metadata extraction, and retrieval
│   └── data/
│       ├── no_hope/
│       │   └── the_shadow_inside/   # Album folder
│       │       └── *.txt            # Song lyrics
│       └── ruben_du_pon/
│           └── *.txt                # Song lyrics (no album)
├── Dockerfile
├── compose.yaml
└── requirements.txt
```

### Data directory conventions

The file structure under `app/data/` determines the metadata attached to each song:

| Structure                          | Artist     | Album     | Title    |
| ---------------------------------- | ---------- | --------- | -------- |
| `data/<artist>/<song>.txt`         | `<artist>` | None      | `<song>` |
| `data/<artist>/<album>/<song>.txt` | `<artist>` | `<album>` | `<song>` |

Underscores in folder and file names are replaced with spaces, and each word is capitalised. For example, `the_shadow_inside/some_song.txt` becomes album _"The Shadow Inside"_ with title _"Some Song"_.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)

### Running the project

```bash
docker compose up --build
```

This starts two services:

- **`api`** — the FastAPI application, available at `http://localhost:8000`
- **`llm`** — an Ollama instance that pulls and serves `qwen2.5:3b`, available at `http://localhost:8001`

> **Note:** The first startup may take a few minutes as Ollama downloads the model.

## API

### `GET /`

Health check endpoint.

**Response:**

```json
{ "message": "Hello World!" }
```

---

### `POST /ask`

Ask a question about the song lyrics.

**Request body:**

```json
{ "question": "What themes does No Hope explore in The Shadow Inside?" }
```

**Response:**

```json
{ "answer": "..." }
```

**Example with curl:**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What themes does No Hope explore in The Shadow Inside?"}'
```

## Adding More Lyrics

Place `.txt` files with lyrics under `app/data/` following the directory convention above, then rebuild the container:

```bash
docker compose up --build
```

## Tech Stack

| Component        | Technology                                                                          |
| ---------------- | ----------------------------------------------------------------------------------- |
| API framework    | [FastAPI](https://fastapi.tiangolo.com/)                                            |
| RAG framework    | [LlamaIndex](https://www.llamaindex.ai/)                                            |
| Embeddings       | [BAAI/bge-small-en](https://huggingface.co/BAAI/bge-small-en)                       |
| LLM              | [Qwen 2.5 3B](https://ollama.com/library/qwen2.5) via [Ollama](https://ollama.com/) |
| Containerisation | Docker Compose                                                                      |

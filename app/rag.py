from pathlib import Path
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")
documents = SimpleDirectoryReader("app/data", recursive=True).load_data()


def format_name(name: str | None) -> str | None:
    """Formats a string without underscores and with each word capitalised.

    Args:
        name (str): The string to be formatted

    Returns:
        str: The formatted string
    """
    if name is None:
        return None
    name = name.replace("_", " ")
    return " ".join(word.capitalize() for word in name.split())


# Add metadata based on file structure
for doc in documents:
    path = Path(doc.metadata["file_path"])
    parts = path.parts

    try:
        data_index = parts.index("data")
        relative_parts = parts[data_index + 1 :]
    except ValueError:
        relative_parts = parts

    if len(relative_parts) == 2:
        artist, filename = relative_parts
        album = None
    elif len(relative_parts) >= 3:
        artist, album, filename = relative_parts[:3]
    else:
        continue

    song_title = Path(filename).stem

    doc.metadata["artist"] = format_name(artist)
    doc.metadata["album"] = format_name(album)
    doc.metadata["title"] = format_name(song_title)

index = VectorStoreIndex.from_documents(documents)

retriever = index.as_retriever(similarity_top_k=7)


def retrieve_context(question: str):
    return retriever.retrieve(question)

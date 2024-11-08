# pinecone
DIMENSION: int = 384
METRIC: str = "cosine"


# splitting text
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 20

# embeddings
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

# LLMs
SYSTEM_PROMPT: tuple = (
    "You are an assistant for question-answering tasks."
    "Use the following pieces of retrived context to answer"
    "the question. If you don't know the answer, say that you"
    "don't know. Use three sentences maximum and keep the answer concise."
    "\n\n"
    "{context}"
)
LLM_MODEL: str = "gemma2-9b-it"

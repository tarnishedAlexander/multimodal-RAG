from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from config.settings import GROK_API_KEY, EMBED_MODEL, LLM_MODEL

def configure_llm():
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    Settings.llm = Groq(model=LLM_MODEL, api_key=GROK_API_KEY)
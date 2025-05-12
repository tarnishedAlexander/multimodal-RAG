import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
GROK_API_KEY = os.getenv("GROQ_API_KEY")
S3_INPUT_BUCKET = os.getenv("S3_INPUT_BUCKET")
S3_INPUT_PREFIX = os.getenv("S3_INPUT_PREFIX")
S3_OUTPUT_BUCKET = os.getenv("S3_OUTPUT_BUCKET")
S3_OUTPUT_PREFIX = os.getenv("S3_OUTPUT_PREFIX")

# DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

# Model settings
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")
CHUNK_SIZE = 512
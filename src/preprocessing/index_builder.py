from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from utils.llm_config import configure_llm
from config.settings import CHUNK_SIZE
from utils.logging import setup_logging
import os

logger = setup_logging()

def build_index(pdf_files: list, persist_dir: str):
    try:
        configure_llm()
        logger.info(f"Construyendo índice desde {len(pdf_files)} PDFs")
        documents = SimpleDirectoryReader(input_files=pdf_files).load_data()
        splitter = SentenceSplitter(chunk_size=CHUNK_SIZE)
        nodes = splitter.get_nodes_from_documents(documents)
        vector_index = VectorStoreIndex(nodes)
        os.makedirs(persist_dir, exist_ok=True)
        vector_index.storage_context.persist(persist_dir=persist_dir)
        logger.info(f"Índice guardado en {persist_dir}")

        # Devolver datos del índice para json_formatter
        index_data = {
            'index_id': os.path.basename(persist_dir),
            'metadata': {'pdf_files': pdf_files}
        }
        return index_data
    except Exception as e:
        logger.error(f"Error al construir índice: {e}")
        raise e
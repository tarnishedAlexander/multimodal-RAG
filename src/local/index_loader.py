from llama_index.core import StorageContext, load_index_from_storage
from utils.logging import setup_logging
from utils.llm_config import configure_llm

logger = setup_logging()

def load_index(persist_dir: str):
    """
    Carga un índice desde un directorio persistente.

    Args:
        persist_dir (str): Directorio donde está almacenado el índice.

    Returns:
        VectorStoreIndex: Índice cargado.
    """
    try:
        configure_llm()
        logger.info(f"Cargando índice desde {persist_dir}")
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        logger.info(f"Índice cargado desde {persist_dir}")
        return index
    except Exception as e:
        logger.error(f"Error al cargar índice desde {persist_dir}: {e}")
        raise e
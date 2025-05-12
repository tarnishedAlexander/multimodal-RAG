from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from utils.utils import get_doc_tools
from utils.llm_config import configure_llm
from utils.logging import setup_logging

logger = setup_logging()

def setup_rag_agent(vector_index: VectorStoreIndex):
    logger.info("Setting up RAG agent")
    configure_llm()  # Configura el LLM y el modelo de embedding
    llm = Settings.llm  # Usa el LLM configurado globalmente
    
    if llm is None:
        logger.error("No LLM configured in Settings")
        raise ValueError("LLM not configured. Ensure configure_llm sets Settings.llm correctly.")
    
    # Agrupar nodos por documento
    doc_nodes = {}
    for node in vector_index.docstore.docs.values():
        doc_id = node.metadata.get("doc_id", "default")
        if doc_id not in doc_nodes:
            doc_nodes[doc_id] = []
        doc_nodes[doc_id].append(node)
    
    logger.info(f"Found {len(doc_nodes)} documents with node counts: {[len(nodes) for nodes in doc_nodes.values()]}")
    
    # Crear herramientas para cada documento
    all_tools = []
    for doc_id, nodes in doc_nodes.items():
        try:
            vector_tool, summary_tool = get_doc_tools(nodes, doc_id)
            all_tools.extend([vector_tool, summary_tool])
        except Exception as e:
            logger.error(f"Error al crear herramientas para doc_id {doc_id}: {e}")
            raise
    
    # Crear índice de objetos para herramientas
    obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)
    obj_retriever = obj_index.as_retriever(similarity_top_k=3)
    
    # Inicializar agente
    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_retriever,
        llm=llm,  # Usa el LLM de Settings
        system_prompt="You are an agent designed to answer queries over a set of given papers. Use the provided tools.",
        verbose=True
    )
    agent = AgentRunner(agent_worker)
    logger.info("RAG agent setup complete")
    return agent
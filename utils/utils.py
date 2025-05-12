from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import VectorStoreIndex, SummaryIndex
from utils.logging import setup_logging

logger = setup_logging()

def get_doc_tools(nodes, doc_id):
    try:
        logger.info(f"Creating tools for doc_id: {doc_id}, nodes: {len(nodes)}")
        # Herramienta de búsqueda vectorial
        vector_index = VectorStoreIndex(nodes)
        vector_query_engine = vector_index.as_query_engine(similarity_top_k=3)
        vector_tool = QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name=f"vector_tool_{doc_id}",
                description=f"Tool for vector search over document {doc_id}"
            )
        )

        # Herramienta de resumen
        summary_index = SummaryIndex(nodes)
        summary_query_engine = summary_index.as_query_engine()
        summary_tool = QueryEngineTool(
            query_engine=summary_query_engine,
            metadata=ToolMetadata(
                name=f"summary_tool_{doc_id}",
                description=f"Tool for summarizing document {doc_id}"
            )
        )

        return vector_tool, summary_tool
    except Exception as e:
        logger.error(f"Error in get_doc_tools for doc_id {doc_id}: {e}")
        raise